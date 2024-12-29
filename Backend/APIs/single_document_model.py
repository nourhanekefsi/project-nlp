import os
import json
import collections
from transformers import AutoTokenizer

# Charger le tokenizer de DistilBERT
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

def read_documents(json_file_path):
    """
    Lit le fichier JSON, extrait les ids et les chemins des fichiers, lit le contenu de chaque fichier,
    et retourne un dictionnaire associant chaque id à son contenu.

    :param json_file_path: Chemin du fichier JSON contenant les métadonnées des documents (id, chemin du fichier).
    :return: Un dictionnaire {id: contenu du document}.
    """
    try:
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            documents = json.load(json_file)
        
        doc_contents = {}
        for doc in documents:
            doc_id = doc.get("id")
            file_path = doc.get("file_path")
            # Vérification de l'existence du fichier et des informations nécessaires
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
    Applique le prétraitement aux documents :
    - Tokenisation (utilisation de DistilBERT)
    - Construction du vocabulaire global à partir des tokens

    :param documents_content: Dictionnaire {id: contenu brut des documents}.
    :return: Dictionnaire avec le contenu prétraité et le vocabulaire global sous forme de Counter.
    """
    vocabulary = collections.Counter()
    preprocessed_content = {}

    for doc_id, content in documents_content.items():
        # Tokenisation du contenu du document avec gestion de la longueur des séquences
        tokens = tokenizer(content, truncation=True, padding=True, max_length=512, return_tensors="pt")
        
        # Enregistrer les tokens sous forme de dictionnaire avec input_ids et attention_mask
        preprocessed_content[doc_id] = {
            'input_ids': tokens['input_ids'].squeeze().tolist(),  # Convertir en liste simple
            'attention_mask': tokens['attention_mask'].squeeze().tolist()  # Convertir en liste simple
        }
        
        # Mise à jour du vocabulaire global
        vocabulary.update(tokens['input_ids'].squeeze().tolist())

    return preprocessed_content, vocabulary

def preprocess_documents_doc(new_doc):
    """
    Applique le prétraitement aux documents :
    - Tokenisation (utilisation de DistilBERT)
    - Construction du vocabulaire global à partir des tokens

    :param documents_content: Dictionnaire {id: contenu brut des documents}.
    :return: Dictionnaire avec le contenu prétraité et le vocabulaire global sous forme de Counter.
    """
    vocabulary = collections.Counter()

        # Tokenisation du contenu du document avec gestion de la longueur des séquences
    tokens = tokenizer(new_doc, truncation=True, padding=True, max_length=512, return_tensors="pt")
        
        # Enregistrer les tokens sous forme de dictionnaire avec input_ids et attention_mask
    preprocessed_content = {
        'input_ids': tokens['input_ids'].squeeze().tolist(),  # Convertir en liste simple
        'attention_mask': tokens['attention_mask'].squeeze().tolist()  # Convertir en liste simple
    }
        
        # Mise à jour du vocabulaire global
    vocabulary.update(tokens['input_ids'].squeeze().tolist())

    return preprocessed_content, vocabulary


from transformers import AutoTokenizer, AutoModel
import torch
import json

# Charger le modèle et le tokenizer DistilBERT
MODEL_NAME = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME)



def create_distilbert_embeddings_doc(tokens):
    """
    Utilise DistilBERT pour calculer des embeddings pour chaque document en moyennant les embeddings des tokens.

    :param doc_contents: Dictionnaire {id: contenu prétraité des documents (tokens)}.
    :param output_file: Nom du fichier JSON où les embeddings seront enregistrés.
    """
    try:
        # Vérification que tokens est bien un dictionnaire avec 'input_ids' et 'attention_mask'
        input_ids = tokens['input_ids']
        attention_mask = tokens['attention_mask']

        # Calcul des embeddings avec le modèle DistilBERT
        with torch.no_grad():
            outputs = model(
                input_ids=torch.tensor([input_ids]),  # Ajouter une dimension batch
                attention_mask=torch.tensor([attention_mask])  # Ajouter une dimension batch
            )
            embeddings = outputs.last_hidden_state.mean(dim=1)  # Moyenne des embeddings des tokens

        # Retourner l'embedding sous forme de liste
        return embeddings.squeeze().tolist()

    except Exception as e:
        print(f"Une erreur s'est produite lors du calcul de l'embedding : {e}")
        return None

        
import csv
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json


def compute_similarity_for_document(document_id, vector_file="../model/distilbert_vectors.json"):
    """
    Calcule la similarité cosinus entre un document spécifique et tous les autres documents.

    :param document_id: ID du document pour lequel calculer les similarités.
    :param vector_file: Nom du fichier JSON contenant les vecteurs des documents.
    :return: Liste des similarités entre le document spécifié et les autres documents.
    """
    try:
        # Charger les vecteurs depuis le fichier JSON
        with open(vector_file, 'r', encoding='utf-8') as json_file:
            document_vectors = json.load(json_file)

        # Vérifier que le document spécifié existe
        doc_ids = list(document_vectors.keys())
        if str(document_id) not in doc_ids:
            raise ValueError(f"L'ID du document {document_id} n'existe pas dans les données.")

        # Convertir les vecteurs en matrice numpy
        vectors = np.array([document_vectors[doc_id] for doc_id in doc_ids])
        document_index = doc_ids.index(str(document_id))  # Récupérer l'index du document cible

        # Calculer la matrice de similarité cosinus
        similarity_matrix = cosine_similarity(vectors)

        # Ligne correspondant au document cible (similitudes avec les autres documents)
        similarity_line = similarity_matrix[document_index].tolist()

        # Ajouter l'ID du document comme premier élément de la ligne
        result = [document_id] + similarity_line

        return result

    except Exception as e:
        raise ValueError(f"Erreur lors du calcul des similarités: {e}")
    
def get_top_similar_documents_with_scores(embedding, threshold, vector_file="../model/distilbert_vectors.json"):
    """
    Calcule la similarité cosinus entre un embedding donné et les vecteurs existants,
    puis retourne les IDs et les scores des documents dont la similarité dépasse un seuil donné.

    :param embedding: Vecteur embedding du document (liste ou numpy array).
    :param vector_file: Nom du fichier JSON contenant les vecteurs des documents.
    :param threshold: Seuil de similarité à partir duquel les documents seront considérés comme similaires.
    :return: Liste de tuples [(id_document, similarité_cosinus), ...] dont les similarités sont supérieures au seuil.
    """
    try:
        # Charger les vecteurs depuis le fichier JSON
        with open(vector_file, 'r', encoding='utf-8') as json_file:
            document_vectors = json.load(json_file)
        
        # Extraire les IDs et les vecteurs existants
        doc_ids = list(document_vectors.keys())
        vectors = np.array([document_vectors[doc_id] for doc_id in doc_ids])
        
        # Convertir l'embedding d'entrée en numpy array
        query_vector = np.array(embedding).reshape(1, -1)
        
        # Calculer la similarité cosinus entre le vecteur d'entrée et les vecteurs existants
        similarities = cosine_similarity(query_vector, vectors).flatten()
        
        # Filtrer les documents dont la similarité dépasse le seuil
        similar_docs = [(doc_ids[i], similarities[i]) for i in range(len(similarities)) if similarities[i] >= threshold]

        # Trier les documents par similarité en ordre décroissant
        similar_docs_sorted = sorted(similar_docs, key=lambda doc: doc[1], reverse=True)
        return similar_docs_sorted

    except Exception as e:
        print(f"Une erreur s'est produite lors du calcul des similarités : {e}")
        return []



def save_sorted_similarities_from_matrix(matrix_file="../model/document_similarity_matrix.csv", output_file="../model/sorted_document_similarities.csv"):
    """
    Enregistre dans un fichier CSV les IDs des documents les plus similaires pour chaque document,
    triés par similarité décroissante, à partir d'une matrice de similarité déjà calculée.

    :param matrix_file: Nom du fichier CSV contenant la matrice de similarité.
    :param output_file: Nom du fichier CSV pour enregistrer les similarités triées (seulement les IDs).
    """
    try:
        # Vérifier que le fichier source existe
        if not os.path.exists(matrix_file):
            raise FileNotFoundError(f"Le fichier source {matrix_file} est introuvable.")
        
        # Charger la matrice de similarité depuis le fichier CSV
        with open(matrix_file, 'r', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            rows = list(reader)

        # Vérifier si la matrice contient des données valides
        if not rows or len(rows) < 2:
            raise ValueError("Le fichier de matrice de similarité est vide ou mal formaté.")

        # Extraire les IDs des documents (en-tête)
        doc_ids = rows[0][1:]  # Les colonnes après "Document"
        if not doc_ids:
            raise ValueError("Aucun document trouvé dans la matrice de similarité.")

        # Préparer les similarités triées (seulement les IDs)
        sorted_similarities = []
        for i, row in enumerate(rows[1:]):  # Parcourir les lignes sauf l'en-tête
            doc_id = row[0]
            similarities = [(doc_ids[j], float(row[j + 1])) for j in range(len(doc_ids))]

            # Trier les similarités par ordre décroissant
            sorted_doc_ids = [sim_doc_id for sim_doc_id, _ in sorted(similarities, key=lambda x: x[1], reverse=True)]
            sorted_similarities.append((doc_id, sorted_doc_ids))

        # Enregistrer les IDs triés dans un fichier CSV
        with open(output_file, 'w', encoding='utf-8', newline='') as csv_file:
            writer = csv.writer(csv_file)

            # Écrire l'en-tête (Document + Liste des IDs des documents similaires)
            header = ["Document"] + [f"Similar Doc {i+1}" for i in range(len(doc_ids))]
            writer.writerow(header)

            # Écrire les similarités triées pour chaque document
            for doc_id, sorted_doc_ids in sorted_similarities:
                writer.writerow([doc_id] + sorted_doc_ids)

        print(f"Les similarités triées ont été enregistrées dans le fichier {output_file}.")

    except Exception as e:
        raise RuntimeError(f"Une erreur s'est produite lors de la sauvegarde des similarités triées : {e}")



