import os
import json
import re
import collections
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import unicodedata
import nltk

import re

def clean_document(text):
    
    # Supprimer les mentions de copyright
    text = re.sub(r"©\s?\d{4}(?:\s?-\s?\d{4})?", "", text)  # Suppression du symbole © et des années
    text = re.sub(r"all rights reserved", "", text, flags=re.IGNORECASE)  # Mention de droits réservés
    text = re.sub(r"copyright .*?\.", "", text, flags=re.IGNORECASE)  # Mention 'copyright' suivie d'une phrase
    
    # Supprimer toutes les phrases de type "sign up", "sign in", ou similaires
    text = re.sub(r"\b(?:sign up|sign in|register|subscribe|join)\b.*?[.!?]", "", text, flags=re.IGNORECASE)
    
    # Nettoyage des espaces superflus
    text = re.sub(r"\s+", " ", text).strip()
    
    return text


def read_documents(json_file_path):
   
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


def normalize_text(text):
    
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)  # Supprime les caractères non alphabétiques
    text = re.sub(r'\s+', ' ', text).strip()  # Supprime les espaces multiples
    return text


def preprocess_documents(documents_content):
    """
    Applique le prétraitement aux documents :
    - Normalisation (suppression des accents, caractères spéciaux)
    - Tokenisation
    - Suppression des stopwords
    - Conversion en minuscules
    - Lemmatisation

    :param documents_content: Dictionnaire {id: contenu brut}.
    :return: Contenu prétraité et vocabulaire global.
    """
    lemmatizer = WordNetLemmatizer()
    stop_words = nltk.corpus.stopwords.words('english')
    vocabulary = collections.Counter()

    preprocessed_content = {}

    for doc_id, content in documents_content.items():
        content = clean_document(content)
        # Normalisation du texte
        content = normalize_text(content)

        # Tokenisation
        tokens = nltk.RegexpTokenizer(r'\w+').tokenize(content)

        # Suppression des stopwords et conversion en minuscules
        tokens = [token.lower() for token in tokens if token.lower() not in stop_words]

        # Lemmatisation
        tokens = [lemmatizer.lemmatize(token) for token in tokens]

        # Mise à jour des résultats
        preprocessed_content[doc_id] = tokens
        vocabulary.update(tokens)

    return preprocessed_content, vocabulary


def save_preprocessed_data(preprocessed_content, output_file1="tokens_docs.json"):
    """
    Sauvegarde le contenu prétraité et le vocabulaire dans un fichier JSON.

    :param preprocessed_content: Dictionnaire {id: contenu prétraité}.
    :param output_file: Chemin du fichier de sortie.
    """
    data_to_save = {
        "preprocessed_content": preprocessed_content,
    }

    try:
        with open(output_file1, 'w', encoding='utf-8') as json_file:
            json.dump(data_to_save, json_file, indent=4, ensure_ascii=False)
        print(f"Les contenus prétraités ont été enregistrés dans le fichier : {output_file1}")
    except Exception as e:
        print(f"Une erreur s'est produite lors de la sauvegarde des données : {e}")

def save_vocabulary(preprocessed_content, output_file2="tokens_corpus.json"):
    data_to_save = {
        "vocabulary": list(vocabulary.keys())
    }

    try:
        with open(output_file2, 'w', encoding='utf-8') as json_file:
            json.dump(data_to_save, json_file, indent=4, ensure_ascii=False)
        print(f"Le vocabulaire a été enregistré dans le fichier : {output_file2}")
    except Exception as e:
        print(f"Une erreur s'est produite lors de la sauvegarde des données : {e}")


# Application principale
if __name__ == "__main__":
    json_file_path = "../model/all_documents.json"
    documents_content = read_documents(json_file_path)

    if documents_content:
        preprocessed_content, vocabulary = preprocess_documents(documents_content)
        save_preprocessed_data(preprocessed_content)
        save_vocabulary(vocabulary)