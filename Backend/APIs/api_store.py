import io
from PyPDF2 import PdfReader
import os
import json
from fastapi import APIRouter, Form, HTTPException, Request, UploadFile
from typing import Optional
import csv
from single_document_model import (
    preprocess_documents_doc,
    create_distilbert_embeddings_doc,
    compute_similarity_for_document,
    save_sorted_similarities_from_matrix
)

from nltk_tokenizer import (
        main
)

uploadApi = APIRouter()

@uploadApi.post("")
async def upload_and_process(
    request: Request,
    file: Optional[UploadFile] = None,
    category: str = Form(...),
    title: str = Form(...),
    author: str = Form(...),
    content: Optional[str] = Form(None),
):
    try:
        # Paths to the required files
        metadata_file = "../model/all_documents.json"
        preprocessed_content_file = "../model/preprocessed_content.json"
        vector_file = "../model/distilbert_vectors.json"
        similarity_matrix_file = "../model/document_similarity_matrix.csv"
        sorted_similarity_file = "../model/sorted_document_similarities.csv"

        # Load or initialize the metadata
        documents = []
        if os.path.exists(metadata_file):
            with open(metadata_file, "r", encoding="utf-8") as metadata_fp:
                documents = json.load(metadata_fp)

        # Check or create the category directory
        category_path = f"../corpus/UserDocs/{category}"
        os.makedirs(category_path, exist_ok=True)

        # Handle file upload
        if file:
            # Save the uploaded PDF file
            file_path = os.path.join(category_path, f"{title}.pdf")
            content = await file.read()

            # Save the PDF as a file
            with open(file_path, "wb") as f:
                f.write(content)

            # Convert PDF content to text (for processing, not saving)
            pdf_file = io.BytesIO(content)  # Create a file-like object from bytes
            pdf_reader = PdfReader(pdf_file)

            # Extract text from the PDF (e.g., all pages)
            document_content = ""
            for page in pdf_reader.pages:
                document_content += page.extract_text()

            

        elif content:
            # If no file is uploaded, save content as a txt file (optional, not necessary if only processing)
            file_path = os.path.join(category_path, f"{title}.txt")
            document_content = content

            with open(file_path, "w", encoding="utf-8") as txt_file:
                txt_file.write(document_content)

        else:
            raise HTTPException(status_code=400, detail="No file or content provided.")

        # Get the base URL and construct the file URL
        base_url = str(request.base_url).rstrip("/")
        updated_path = file_path.replace("\\", "/")
        updated_path = updated_path.replace("../corpus", "corpus")
        url = f"{base_url}/{updated_path}"

        # Generate a new ID for the document
        new_id = max((doc["id"] for doc in documents), default=0) + 1

        # Add the document to metadata
        new_document = {
            "id": new_id,
            "title": title,
            "author": author,
            "type": "document",
            "categorie": category,
            "file_path": file_path,
            "url": url,
        }
        documents.append(new_document)

        # Save updated metadata
        with open(metadata_file, "w", encoding="utf-8") as metadata_fp:
            json.dump(documents, metadata_fp, indent=4)

        # Preprocess the document and save it's vocabulary
        preprocessed_content, vocabulary = preprocess_documents_doc(document_content)

        # Update the preprocessed content file
        preprocessed_data = {}
        if os.path.exists(preprocessed_content_file):
            with open(preprocessed_content_file, "r", encoding="utf-8") as preprocessed_fp:
                preprocessed_data = json.load(preprocessed_fp)

        if "preprocessed_content" not in preprocessed_data:
            preprocessed_data["preprocessed_content"] = {}

        preprocessed_data["preprocessed_content"][str(new_id)] = {
            "input_ids": preprocessed_content,
            "vocabulary": vocabulary,
        }

        with open(preprocessed_content_file, "w", encoding="utf-8") as preprocessed_fp:
            json.dump(preprocessed_data, preprocessed_fp, indent=4)

        # Generate vectors for the document
        vector = create_distilbert_embeddings_doc(preprocessed_content)

        # Update the vector file
        vectors = {}
        if os.path.exists(vector_file):
            with open(vector_file, "r", encoding="utf-8") as vector_fp:
                vectors = json.load(vector_fp)

        vectors[str(new_id)] = vector

        with open(vector_file, "w", encoding="utf-8") as vector_fp:
            json.dump(vectors, vector_fp, indent=4)

        # Compute similarities for the new document
        similarity_line = compute_similarity_for_document(new_id, vector_file=vector_file)

        # First, read the existing similarity matrix into memory
        with open(similarity_matrix_file, "r", newline="") as csv_file: # read
            reader = csv.reader(csv_file)
            matrix = [row for row in reader]

        # Add the new similarity line as a new row (horizontally)
        matrix.append(similarity_line)

        # Add the new similarity line as a new column (vertically) in all existing rows
        for i, row in enumerate(matrix):
            row.append(similarity_line[i])

        # Now write the updated matrix back to the CSV file
        with open(similarity_matrix_file, "w", newline="") as csv_file: # write
            writer = csv.writer(csv_file)
            writer.writerows(matrix)

        # Save sorted similarities
        save_sorted_similarities_from_matrix(similarity_matrix_file, sorted_similarity_file)
        print(f"Similarity Matrix updated")

        # Save tokens
        main(single_document=document_content,DocId=new_id)
        print(f"Tokens saved")

        return {"message": "File uploaded and processed successfully.", "document_url": url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")






