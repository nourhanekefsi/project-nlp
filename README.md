# Project 
## Description
## preparing the environment 
to run this app, open terminal or cmd and do as follow:

git clone https://github.com/nourhanekefsi/project-nlp.git

pip install -r requirements.txt

Ensure the following Python libraries are installed:
FastAPI
nltk
matplotlib
wordcloud
scikit-learn
pandas
numpy ...

import nltk
nltk.download('punkt')
nltk.download('stopwords')

## Run the app
1st of all in the terminal run 

cd project-nlp/backend/APIs

uvicorn main:app --reload

open another tab of terminal

cd project-nlp/frontend

npm install

npm start
