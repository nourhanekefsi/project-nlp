Structure de fichier

api_store.py :
Implémente le Endpoint /upload.
Gère les téléchargements de fichiers, la saisie de métadonnées et l'intégration dans le corpus.

main.py :
Contient cinq fonctionnalités principales :
Renvoyer les métadonnées du document.
Renvoyer le contenu du document.
Renvoyer les détails du document et leurs documents similaires.
Prétraiter et recommander des documents similaires pour un nouveau document
Générer un wordCloud pour un identifiant de document spécifique.

nltk_tokenizer.py :
Prétraite l'ensemble du corpus et chaque document à l'aide de NLTK.
Génère des tokens pour chaque document stockés sur tokens_doocs.json et pour tout le corpus a la fois sur tokens_corpus.json.

visuals.ipynb :
Génère des visualisations, notamment des wordCloud et d'autres représentations graphiques

single_document_model.py :
Contient des fonctions de recommandation qui gèrent le preprcessing, la vectorisation et les calculs de similarité pour des documents individuels
