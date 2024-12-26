import csv
from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import json
import os
from transformers import AutoTokenizer
from model_recommndation import preprocess_documents_doc
from model_recommndation import create_distilbert_embeddings_doc
from model_recommndation import get_top_similar_documents_with_scores

# Define a Pydantic model for the request body
class DocumentRequest(BaseModel):
    author: str
    category: str
    title: str
    content: str

app = FastAPI()

# **1. Récupérer les métadonnées des documents (sans file path)**
@app.get("/documents")
def get_all_documents():
    try:
        with open("all_documents.json", "r") as file:
            documents = json.load(file)
        for doc in documents:
            doc.pop("file_path", None)
        return documents
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")

# **2. Récupérer le contenu d’un document spécifique**
@app.get("/document/{doc_id}")
def get_document_content(doc_id: int):
    try:
        with open("all_documents.json", "r") as file:
            documents = json.load(file)
        document = next((doc for doc in documents if doc["id"] == doc_id), None)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        with open(document["file_path"], "r") as doc_file:
            content = doc_file.read()
        return {"id": doc_id, "content": content}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")

# **3. Récupérer les détails d’un document avec les documents similaires**
@app.get("/document/{doc_id}/details")
def get_document_details(doc_id: int):
    try:
        # Charger les métadonnées des documents depuis le fichier JSON
        with open("all_documents.json", "r") as file:
            documents = json.load(file)
        
        # Trouver le document principal par ID
        document = next((doc for doc in documents if doc["id"] == doc_id), None)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Lire le contenu du document principal
        try:
            with open(document["file_path"], "r") as doc_file:
                content = doc_file.read()
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="Document file not found")
        
        # Ajouter le contenu au document principal
        main_document = {
            "id": document["id"],
            "title": document["title"],
            "author": document["author"],
            "content": content
        }

        # Initialiser une liste pour les documents similaires
        similar_docs = []

        # Charger les 10 documents les plus similaires depuis sorted_document_similarities.csv
        with open("sorted_document_similarities.csv", "r") as csv_file:
            reader = csv.reader(csv_file)
            headers = next(reader)  # Lire l'en-tête
            for row in reader:
                if int(row[0]) == doc_id:  # Trouver la ligne correspondant à doc_id
                    similar_doc_ids = [int(row[i]) for i in range(1, 11)]  # Extraire les 10 IDs similaires
                    break
            else:
                raise HTTPException(status_code=404, detail="No similar documents found")

        # Charger la matrice de similarité depuis document_similarity_matrix.csv
        similarity_scores = {}
        with open("document_similarity_matrix.csv", "r") as csv_file:
            reader = csv.reader(csv_file)
            headers = next(reader)  # Lire l'en-tête (les IDs des documents)
            for row in reader:
                if int(row[0]) == doc_id:  # Trouver la ligne correspondant à doc_id
                    similarity_scores = {int(headers[i]): float(row[i]) for i in range(1, len(headers))}
                    break

        # Pour chaque ID similaire, récupérer les métadonnées et la similarité
        for similar_id in similar_doc_ids:
            similar_document = next((doc for doc in documents if doc["id"] == similar_id), None)
            if similar_document:
                similar_docs.append({
                    "id": similar_id,
                    "title": similar_document["title"],
                    "similarity": similarity_scores.get(similar_id, 0.0),  # Récupérer la similarité
                })

        # Trier les documents similaires par similarité décroissante
        similar_docs_sorted = sorted(similar_docs, key=lambda doc: doc["similarity"], reverse=True)

        # Retourner les résultats
        return {
            "document": main_document,
            "similar_documents": similar_docs_sorted
        }

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=f"Required file not found: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")




# **4. Analyser un document uploadé sans le stocker**

@app.post("/upload")
async def upload_file_or_text(
    file: UploadFile = None,
    text: str = Form(None)
):
    try:
        # Vérifier qu'un seul des deux est fourni
        if file and text:
            raise HTTPException(status_code=400, detail="Provide either a file or text, not both.")
        if not file and not text:
            raise HTTPException(status_code=400, detail="No file or text provided.")
        
        # Traiter le contenu (fichier ou texte)
        if file:
            content = await file.read()
            try:
                document_content = content.decode("utf-8")
            except UnicodeDecodeError:
                raise HTTPException(status_code=400, detail="File must be UTF-8 encoded.")
        else:
            document_content = text

        if not document_content.strip():
            raise HTTPException(status_code=400, detail="Provided file or text is empty.")

        # Prétraitement et génération des vecteurs
        preprocessed_content, _ = preprocess_documents_doc(document_content)
        embedding = create_distilbert_embeddings_doc(preprocessed_content)
        top_similar_docs = get_top_similar_documents_with_scores(embedding, vector_file="distilbert_vectors.json", top_k=10)
        
        try:
            with open("all_documents.json", "r", encoding="utf-8") as meta_file:
                all_metadata = json.load(meta_file)
        except FileNotFoundError:
            raise HTTPException(status_code=500, detail="Metadata file 'all_documents.json' not found.")
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail="Error decoding 'all_documents.json'.")
        
        top_similar_documents = []
        for s_id, similarity in top_similar_docs:
            # Convertir s_id en entier pour correspondre à l'id dans all_metadata
            s_id = int(s_id)  # Si s_id est une chaîne de caractères ou un float, cette conversion est nécessaire
            similar_doc = next((doc for doc in all_metadata if doc["id"] == s_id), None)
            if similar_doc:
                top_similar_documents.append({
                    "id": s_id, 
                    "similarity": similarity,
                    "title": similar_doc["title"],
                    "url": similar_doc["url"],
                })
            else:
                # Ajoutez des logs de débogage pour vérifier si un document n'a pas été trouvé
                print(f"Document with id {s_id} not found in metadata.")
        
        # Retourner la réponse avec les similarités
        return {
            "message": "Document processed successfully.",
            "similar_documents": top_similar_documents
        }

    except HTTPException as http_exc:
        raise http_exc  # Relancer les exceptions HTTP avec leur code
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")