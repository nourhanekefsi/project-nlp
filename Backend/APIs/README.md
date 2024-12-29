# Structure de fichier

## api_store.py :
1.Implémente le Endpoint /upload.

2.Gère les téléchargements de fichiers, la saisie de métadonnées et l'intégration dans le corpus.

## main.py :
### Contient cinq fonctionnalités principales :
1.Renvoyer les métadonnées du document.

2.Renvoyer le contenu du document.

3.Renvoyer les détails du document et leurs documents similaires.

4.Prétraiter et recommander des documents similaires pour un nouveau document

5.Générer un wordCloud pour un identifiant de document spécifique.

## nltk_tokenizer.py :
1.Prétraite l'ensemble du corpus et chaque document à l'aide de NLTK.

2.Génère des tokens pour chaque document stockés sur tokens_doocs.json et pour tout le corpus a la fois sur tokens_corpus.json.

## visuals.ipynb :
Génère des visualisations, notamment des wordCloud et d'autres représentations graphiques

## single_document_model.py :
Contient des fonctions de recommandation qui gèrent le preprcessing, la vectorisation et les calculs de similarité pour des documents individuels
