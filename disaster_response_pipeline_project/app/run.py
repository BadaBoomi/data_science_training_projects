import json
import plotly
import pandas as pd

from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

from flask import Flask
from flask import render_template, request, jsonify
from plotly.graph_objs import Bar, Pie
# from sklearn.externals import joblib
import joblib
from sqlalchemy import create_engine
# from ModelSingleton import ModelSingleton

app = Flask(__name__)


def tokenize(text):
    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()
    
    clean_tokens = []
    for tok in tokens:
        clean_tok = lemmatizer.lemmatize(tok).lower().strip()
        clean_tokens.append(clean_tok)
    return clean_tokens

# load data
engine = create_engine('sqlite:///../data/DisasterResponse.db')
df = pd.read_sql_table('CleanedData', engine)
# df = pd.read_sql_query('select * from CleanedData', engine)

# load model
print('loading model')
model = joblib.load("../models/classifier.pkl")
print('model loaded')


# index webpage displays cool visuals and receives user input text for model
@app.route('/')
@app.route('/index')
def index():
    
    # extract data needed for visuals
    # TODO: Below is an example - modify to extract data for your own visuals
    genre_counts = df.groupby('genre').count()['message']
    genre_names = list(genre_counts.index)
    
    # create visuals
    # TODO: Below is an example - modify to create your own visuals
    graphs = [
        {
            'data': [
                Bar(
                    x=genre_names,
                    y=genre_counts
                )
            ],

            'layout': {
                'title': 'Distribution of Message Genres',
                'yaxis': {
                    'title': "Count"
                },
                'xaxis': {
                    'title': "Genre"
                }
            }
        }
    ]

    ## Most common categories
    df_cat = df[df.columns[4:]]
    cat_sums = df_cat.sum(axis=0).sort_values(ascending=False)
    labels = list(cat_sums[:10].keys())
    values = list(cat_sums[:10])
    graph_most_common = {
            'data': [
                Pie(
                    labels=labels,
                    values=values
                )
            ],

            'layout': {
                'title': 'Distribution of Most Common Categories',
                'hole': .3
            }
        }
    
    graphs.append(graph_most_common)

    # encode plotly graphs in JSON
    ids = ["graph-{}".format(i) for i, _ in enumerate(graphs)]
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
    
    # render web page with plotly graphs
    return render_template('master.html', ids=ids, graphJSON=graphJSON)


# web page that handles user query and displays model results
@app.route('/go')
def go():
    print('entering go')
    # save user input in query
    query = request.args.get('query', '') 

    # use model to predict classification for query
    classification_labels = model.predict([query])[0]
    classification_results = dict(zip(df.columns[4:], classification_labels))
    print('classification_results: {classification_results}')

    # This will render the go.html Please see that file. 
    return render_template(
        'go.html',
        query=query,
        classification_result=classification_results
    )

# # call for evaluation in transformer model
# @app.route('/go_trans')
# def go_trans():
#     print('entering go_trans')
#     # save user input in query
#     query = request.args.get('query', '') 

#     # use transformer model to predict classification for query
#     print('eval query')
#     model = ModelSingleton()
#     classification_labels = model.eval_message( query)
#     print('classification_labels: {classification_labels}')
#     classification_results = dict(zip(df.columns[4:], classification_labels))
#     print('classification_results: {classification_results}')

#     # This will render the go.html Please see that file. 
#     return render_template(
#         'go.html',
#         query=query,
#         classification_result=classification_results
#     )



def main():
    app.run(host='0.0.0.0', port=3001, debug=False)


if __name__ == '__main__':
    main()