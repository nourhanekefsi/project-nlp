from fastapi import FastAPI, UploadFile, Form, HTTPException
import json
import os
import csv
from model_recommndation import (
    preprocess_documents_doc,
    create_distilbert_embeddings_doc,
    compute_similarity_for_document,
    save_sorted_similarities_from_matrix
)

app = FastAPI()


@app.post("/upload_and_process")
async def upload_and_process(
    file: UploadFile,
    category: str = Form(...),
    title: str = Form(...),
    author: str = Form(...),
    type: str = Form(...),  # User-provided type
    url: str = Form("")
):
    try:
        # Paths to the required files
        metadata_file = "all_documents.json"
        preprocessed_content_file = "preprocessed_content.json"
        vector_file = "distilbert_vectors.json"
        similarity_matrix_file = "document_similarity_matrix.csv"
        sorted_similarity_file = "sorted_document_similarities.csv"

        # Load or initialize the metadata
        documents = []
        if os.path.exists(metadata_file):
            with open(metadata_file, "r", encoding="utf-8") as metadata_fp:
                documents = json.load(metadata_fp)

        # Check if the category exists or create a new one
        base_dirs = ["corpus/article_actualite", "corpus/articles_presses"]
        category_path = None
        for base_dir in base_dirs:
            potential_path = os.path.join(base_dir, category)
            if os.path.exists(potential_path):
                category_path = potential_path
                break

        if not category_path:
            category_path = os.path.join(base_dirs[0], category)  # Default to "article_actualite"
            os.makedirs(category_path, exist_ok=True)

        # Save the uploaded file in the determined category folder
        file_path = os.path.join(category_path, f"{title}.txt")
        content = await file.read()  # Read the content outside the file-writing context
        with open(file_path, "wb") as f:
            f.write(content)

        # Generate a new ID for the document
        new_id = max((doc["id"] for doc in documents), default=0) + 1

        # Add the document to metadata
        new_document = {
            "id": new_id,
            "title": title,
            "author": author,
            "type": type,  # User-provided type
            "categorie": category,
            "file_path": file_path,
            "url": url
        }
        documents.append(new_document)

        # Save updated metadata
        with open(metadata_file, "w", encoding="utf-8") as metadata_fp:
            json.dump(documents, metadata_fp, indent=4)

        # Preprocess the document
        document_content = content.decode("utf-8")  # Decode content as UTF-8 string
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
            "vocabulary": vocabulary
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

        # Append the new similarities to the similarity matrix
        with open(similarity_matrix_file, "a", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(similarity_line)

        # Save sorted similarities
        save_sorted_similarities_from_matrix(similarity_matrix_file, sorted_similarity_file)

        # Verify the sorted similarities
        with open(sorted_similarity_file, "r") as sorted_file:
            sorted_data = sorted_file.read()
            print(f"Contenu du fichier trié :\n{sorted_data}")

        return {"message": "File uploaded and processed successfully.", "document_id": new_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
