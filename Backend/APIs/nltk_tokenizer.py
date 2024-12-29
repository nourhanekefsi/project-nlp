import os
import json
import re
import collections
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import unicodedata
import nltk

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')

def clean_document(text):
    """
    Cleans the document by removing unwanted content such as copyright mentions and sign-up phrases.
    """
    text = re.sub(r"\u00a9\s?\d{4}(?:\s?-\s?\d{4})?", "", text)  # Remove © and years
    text = re.sub(r"all rights reserved", "", text, flags=re.IGNORECASE)
    text = re.sub(r"copyright .*?\.", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\b(?:sign up|sign in|register|subscribe|join)\b.*?[.!?]", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def normalize_text(text):
    """
    Normalizes the text by removing accents and special characters.
    """
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def preprocess_content(content):
    """
    Preprocesses a single document's content by cleaning, normalizing, tokenizing, and lemmatizing.

    :param content: Raw document content as a string.
    :return: List of tokens and vocabulary.
    """
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
    """
    Reads and processes multiple documents from a JSON file containing file paths.

    :param json_file_path: Path to the JSON file containing document metadata.
    :return: Dictionary of document IDs to their content.
    """
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
    """
    Preprocesses multiple documents.

    :param documents_content: Dictionary {id: raw content}.
    :return: Preprocessed content and global vocabulary.
    """
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    vocabulary = collections.Counter()

    preprocessed_content = {}

    for doc_id, content in documents_content.items():
        tokens, doc_vocabulary = preprocess_content(content)
        preprocessed_content[doc_id] = tokens
        vocabulary.update(doc_vocabulary)

    return preprocessed_content, vocabulary

def save_data(preprocessed_content, vocabulary, tokens_file="tokens_docs.json", vocab_file="vocabulary.json"):
    """
    Saves preprocessed content and vocabulary to JSON files.

    :param preprocessed_content: Preprocessed tokens by document (dictionary {id: tokens}).
    :param vocabulary: Vocabulary.
    :param tokens_file: Path to save tokens.
    :param vocab_file: Path to save vocabulary.
    """
    try:
        # Save tokens per document
        tokens_list = [{"id": doc_id, "tokens": tokens} for doc_id, tokens in preprocessed_content.items()]
        with open(tokens_file, 'w', encoding='utf-8') as file:
            json.dump({"documents": tokens_list}, file, indent=4, ensure_ascii=False)
        print(f"Tokens have been saved to: {tokens_file}")

        # Save vocabulary
        with open(vocab_file, 'w', encoding='utf-8') as file:
            json.dump({"vocabulary": list(vocabulary.keys())}, file, indent=4, ensure_ascii=False)
        print(f"Vocabulary has been saved to: {vocab_file}")

    except Exception as e:
        print(f"Error saving data: {e}")


def main(json_file_path=None, single_document=None, DocId=None):
    """
    Main function to process either multiple documents or a single document.

    :param json_file_path: Path to a JSON file containing document metadata.
    :param single_document: Single document content as a string.
    """
    if single_document:
        print("Processing single document...")
        tokens, vocabulary = preprocess_content(single_document)
        save_data({DocId: tokens}, vocabulary)
    elif json_file_path:
        print("Processing documents from JSON file...")
        documents_content = read_documents(json_file_path)
        if documents_content:
            preprocessed_content, vocabulary = preprocess_documents(documents_content)
            save_data(preprocessed_content, vocabulary)
    else:
        print("No input provided. Please provide either a JSON file path or a single document.")

# Example usage
if __name__ == "__main__":
    # Path to the JSON file
    json_file_path = "../model/all_documents.json"

    main(json_file_path=json_file_path)
