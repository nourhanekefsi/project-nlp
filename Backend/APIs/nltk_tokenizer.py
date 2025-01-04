import os
import json
import re
import collections
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import unicodedata
import nltk

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')

def clean_document(text):
    
    # Cleans the document by removing unwanted content such as copyright mentions and sign-up phrases.
    
    text = re.sub(r"\u00a9\s?\d{4}(?:\s?-\s?\d{4})?", "", text)  # Remove © and years
    text = re.sub(r"all rights reserved", "", text, flags=re.IGNORECASE)
    text = re.sub(r"copyright .*?\.", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\b(?:sign up|sign in|register|subscribe|join)\b.*?[.!?]", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def normalize_text(text):
    # Normalizes the text by removing accents and special characters.
    
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def preprocess_content(content):
    # Preprocesses a single document's content by cleaning, normalizing, tokenizing, and lemmatizing.
    # in : content: Raw document content as a string.
    # out : List of tokens and vocabulary.

    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    vocabulary = collections.Counter()

    # Clean and normalize
    content = clean_document(content)
    content = normalize_text(content)

    # Tokenize
    tokens = nltk.RegexpTokenizer(r'\w+').tokenize(content)

    # Remove stopwords and lowercase
    tokens = [token.lower() for token in tokens if token.lower() not in stop_words]

    # Lemmatize
    tokens = [lemmatizer.lemmatize(token) for token in tokens]

    # Update vocabulary
    vocabulary.update(tokens)

    return tokens, vocabulary

def read_documents(json_file_path):
    # Reads and processes multiple documents from a JSON file containing file paths.
    # in : json_file_path: Path to the JSON file containing document metadata.
    # out : Dictionary of document IDs to their content.

    try:
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            documents = json.load(json_file)

        doc_contents = {}
        for doc in documents:
            doc_id = doc.get("id")
            file_path = doc.get("file_path")
            if doc_id and file_path and os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                doc_contents[doc_id] = content
            else:
                print(f"Fichier introuvable ou informations manquantes pour l'id {doc_id}: {file_path}")
        return doc_contents

    except Exception as e:
        print(f"Une erreur s'est produite lors de la lecture des documents : {e}")
        return {}

def preprocess_documents(documents_content):
    # Preprocesses multiple documents.
    # in : documents_content: Dictionary {id: raw content}.
    # out : Preprocessed content and global vocabulary.

    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    vocabulary = collections.Counter()

    preprocessed_content = {}

    for doc_id, content in documents_content.items():
        tokens, doc_vocabulary = preprocess_content(content)
        save_data(tokens, doc_vocabulary)
        vocabulary.update(doc_vocabulary)
    print(f"Vocabulary has been saved to: vocabulary.json")
    print(f"Tokens per document has been saved to: tokens_docs.json")
    return preprocessed_content, vocabulary

def save_data(tokens, vocabulary, tokens_file="tokens_docs.json", vocab_file="vocabulary.json"):
    # Saves preprocessed content and vocabulary to JSON files.
    # in : preprocessed_content: Preprocessed tokens by document (dictionary {id: tokens}).
    # in : vocabulary: Vocabulary.
    # in : tokens_file: Path to save tokens.
    # in : vocab_file: Path to save vocabulary.

    try:
        # Ensure tokens file exists and read existing data if present
        if os.path.exists(tokens_file):
            with open(tokens_file, 'r', encoding='utf-8') as file:
                existing_data = json.load(file)
        else:
            existing_data = []  # If file does not exist, initialize with an empty list.
        doc_id = len(existing_data)+1
        # Append new tokens directly to the array
        tokens_list = {"id": doc_id, "tokens": tokens} 

        existing_data.append(tokens_list)

        # Save updated tokens data directly as an array
        with open(tokens_file, 'w', encoding='utf-8') as file:
            json.dump(existing_data, file, indent=4, ensure_ascii=False)

        # Ensure vocabulary file exists and read existing data if present
        if os.path.exists(vocab_file):
            with open(vocab_file, 'r', encoding='utf-8') as file:
                existing_vocab = json.load(file)
        else:
            existing_vocab = []  # If file does not exist, initialize with an empty list.

        # Append new vocabulary and remove duplicates
        vocabulary_list = list(vocabulary.keys())
        existing_vocab.extend(vocabulary_list)
        existing_vocab = list(set(existing_vocab))  # Remove duplicates

        # Save updated vocabulary data directly as an array (no "vocabulary" wrapper)
        with open(vocab_file, 'w', encoding='utf-8') as file:
            json.dump(existing_vocab, file, indent=4, ensure_ascii=False)

    except Exception as e:
        print(f"Error saving data: {e}")

def saveTokens(json_file_path=None, single_document=None, DocId=None):
    # Main function to process either multiple documents or a single document.
    # in : json_file_path: Path to a JSON file containing document metadata.
    # in : single_document: Single document content as a string.

    if single_document:
        print("Processing single document...")
        tokens, vocabulary = preprocess_content(single_document)
        save_data( tokens, vocabulary)
    elif json_file_path:
        print("Processing documents from JSON file...")
        documents_content = read_documents(json_file_path)
        if documents_content:
            preprocessed_content, vocabulary = preprocess_documents(documents_content)
    else:
        print("No input provided. Please provide either a JSON file path or a single document.")

# Example usage
if __name__ == "__main__":
    # Path to the JSON file
    json_file_path = "../model/all_documents.json"

    saveTokens(json_file_path=json_file_path)


