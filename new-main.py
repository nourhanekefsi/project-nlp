import csv
import json
from io import BytesIO
from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from transformers import AutoTokenizer
import PyPDF2

from model_recommendation import (
    preprocess_documents_doc,
    create_distilbert_embeddings_doc,
    get_top_similar_documents_with_scores
)
from api_store import uploadApi  # Ensure `uploadApi` is correctly defined in api_store

# Définir un model Pydantic pour le request body
class DocumentRequest(BaseModel):
    author: str
    category: str
    title: str
    content: str

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Récupérer les métadonnées des documents
@app.get("/documents")
def get_all_documents():
    try:
        with open("all_documents.json", "r", encoding="utf-8") as file:
            documents = json.load(file)
        for doc in documents:
            doc.pop("file_path", None)
        return documents
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")

# Retourner le lien d'un doc
@app.get("/document/{doc_id}")
def get_document_content(doc_id: int):
    try:
        with open("all_documents.json", "r") as file:
            documents = json.load(file)
        document = next((doc for doc in documents if doc["id"] == doc_id), None)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        return {"id": doc_id, "link": document["url"]}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    
#définir un seuil
threshold: float = 0.4

#Retourner les details d'un document et ses documents les plus similaires en utilisant un seuil
@app.get("/document/{doc_id}/details")
def get_document_details(doc_id: int):  
    try:
        with open("all_documents.json", "r") as file:
            documents = json.load(file)
        document = next((doc for doc in documents if doc["id"] == doc_id), None)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")

        main_document = {
            "id": document["id"],
            "title": document["title"],
            "author": document["author"],
            "link": document["url"]
        }

        similar_docs = []
        with open("sorted_document_similarities.csv", "r") as csv_file:
            reader = csv.reader(csv_file)
            headers = next(reader)
            for row in reader:
                if int(row[0]) == doc_id:
                    similar_doc_ids = [int(row[i]) for i in range(2, len(headers))]
                    break
            else:
                raise HTTPException(status_code=404, detail="No similar documents found")

        similarity_scores = {}
        with open("document_similarity_matrix.csv", "r") as csv_file:
            reader = csv.reader(csv_file)
            headers = next(reader)
            for row in reader:
                if int(row[0]) == doc_id:
                    similarity_scores = {int(headers[i]): float(row[i]) for i in range(1, len(headers))}
                    break

        for similar_id in similar_doc_ids:
            similar_document = next((doc for doc in documents if doc["id"] == similar_id), None)
            if similar_document:
                similarity = similarity_scores.get(similar_id, 0.0)
                if similarity >= threshold:  
                    similar_docs.append({
                        "id": similar_id,
                        "title": similar_document["title"],
                        "similarity": similarity
                    })

        similar_docs_sorted = sorted(similar_docs, key=lambda doc: doc["similarity"], reverse=True)

        return {
            "document": main_document,
            "similar_documents": similar_docs_sorted
        }

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=f"Required file not found: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

# used by function 4
async def extract_text_from_pdf(file_bytes):
    # Wrap the bytes object in a BytesIO stream to make it file-like
    pdf_file = BytesIO(file_bytes)
    
    try:
        # Use a PDF processing library like PyPDF2 to extract text
        reader = PyPDF2.PdfReader(pdf_file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        raise HTTPException(status_code=500, detail="Error extracting text from PDF.")


#Analyser un document uploaded et retourner ses similarités
@app.post("/search")
async def upload_file_or_text(
    file: UploadFile = None,
    text: str = Form(None),
):
    try:
        if file and file.filename == "":
            file = None  

        if file and text:
            raise HTTPException(status_code=400, detail="Provide either a file or text, not both.")
        if not file and not text:
            raise HTTPException(status_code=400, detail="No file or text provided.")
        
        if file:
            content = await file.read()
            document_content = await extract_text_from_pdf(content)
        else:
            document_content = text

        if not document_content.strip():
            raise HTTPException(status_code=400, detail="Provided file or text is empty.")

        # Preprocess, embed, and similar documents
        preprocessed_content, _ = preprocess_documents_doc(document_content)
        embedding = create_distilbert_embeddings_doc(preprocessed_content)
        top_similar_docs = get_top_similar_documents_with_scores(embedding, threshold=threshold, vector_file="distilbert_vectors.json")

        # trouver metadata pour les documents similaires
        with open("all_documents.json", "r", encoding="utf-8") as meta_file:
            all_metadata = json.load(meta_file)

        top_similar_documents = []
        for s_id, similarity in top_similar_docs:
            s_id = int(s_id)
            similar_doc = next((doc for doc in all_metadata if doc["id"] == s_id), None)
            if similar_doc and similarity >= threshold: 
                top_similar_documents.append({
                    "id": s_id, 
                    "similarity": similarity,
                    "title": similar_doc["title"],
                    "url": similar_doc["url"],
                })
        
        return {
            "message": "Document processed successfully.",
            "similar_documents": top_similar_documents
        }

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")




# Include routes from api_store and static files
app.include_router(uploadApi, prefix="/upload")
app.mount("/corpus", StaticFiles(directory="corpus"), name="corpus")
