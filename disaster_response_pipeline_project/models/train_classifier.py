import sys
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import pickle

# imports for normalizing and tokenizing
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk

# imports for pipeline
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV

# nltk downloads
nltk.download(['punkt', 'wordnet', 'averaged_perceptron_tagger', 'stopwords', 'omw-1.4'])

def load_data(database_filepath):
    ''' loads data from sqllite database

    INPUT:
        database_filepath - path to sql db


    OUTPUT:
        X              - pandas dataframe containing the message data
        Y              - pandas dataframe containing the category data
        category_names - list of all category names
    '''
    engine = create_engine(f'sqlite:///{database_filepath}')
    # df = pd.read_sql_query('select * from CleanedData limit 50', engine)
    df = pd.read_sql_query('select * from CleanedData', engine)
    X = df[['message']]
    Y = df[df.columns[4:]]
    category_names = list(Y.columns)

    return X, Y, category_names

def tokenize(text):
    ''' normalizes, removes stopwords and lemmatizes

    INPUT:
        text         - text in English language

    OUTPUT:
        clean_tokens - list of cleaned tokens
    '''

    # Remove punctuation characters
    text = re.sub('[^0-9a-z]+', ' ', text.lower())
    #Split text into words using NLTK
    words = word_tokenize(text)
    # Remove stop words
    words = [w for w in words if w not in stopwords.words("english")]

    lemmatizer = WordNetLemmatizer()

    clean_tokens = []
    for tok in words:
        clean_tok = lemmatizer.lemmatize(tok).strip()
        clean_tokens.append(clean_tok)

    return clean_tokens


def build_model(X_train, y_train):
    ''' builds pipeline and trains model (performs also grid search about some hyper parameters)

    INPUT:
        X_train, y_train : trainingsdat

    OUTPUT:
        trained model
    '''
    pipeline = Pipeline([
        ('features', FeatureUnion([

            ('text_pipeline', Pipeline([
                # ('vect', CountVectorizer(tokenizer=tokenize)),
                ('tfidf', TfidfVectorizer(tokenizer = tokenize, sublinear_tf = True))
            ])),

        ])),

        ('clf', MultiOutputClassifier(estimator=RandomForestClassifier(random_state = 42, \
            n_estimators = 200)))
        ])

    parameters = {
        # 'clf__estimator__n_estimators': [100, 200, 300],
        # 'clf__estimator__criterion': ['gini', 'entropy', 'log_loss'],
        'features__text_pipeline__tfidf__sublinear_tf':[True, False]
        }

    cv = GridSearchCV(pipeline, param_grid=parameters)
    cv.fit(X_train.message, y_train)

    # return pipeline.fit(X_train.message, y_train)
    return cv.best_estimator_


def evaluate_model(model, X_test, y_test, category_names,
                    report_filepath='classification_report.txt'):
    ''' evaluates the trained model on test data

    INPUT:
        model           - trained model
        X_test          - data for prediction
        Y_test          - labeled/real values for categories
        category_names  - list with category names
        report_filepath - path to store the evaluation report

    OUTPUT:
        saves report to file
        returns array with results
    '''
    predicted = model.predict(X_test.message)
    results = []
    for index, y_pred in enumerate(np.transpose(predicted)):
        y_true=y_test.iloc[:, index]
        results.append(f'{category_names[index]}: {classification_report(y_true, y_pred)}')

    with open(report_filepath, "w+") as f:
        f.write(str(results))

    return results




def save_model(model, model_filepath):
    ''' dumps model to file

    INPUT:
        model           - trained model
        model_filepath  - path to store the trained model

    OUTPUT:
        True - if model has been successfully saved to file
    '''
    with open(model_filepath, 'wb') as file:
        pickle.dump(model, file)


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

        print('Building model...')
        model = build_model(X_train, Y_train)

        # print('Training model...')
        # model.fit(X_train, Y_train)
        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)
        print('Trained model saved!')

        print('Evaluating model...')
        results = evaluate_model(model, X_test, Y_test, category_names)
        print(f'evaluation results: {results}')





    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()
