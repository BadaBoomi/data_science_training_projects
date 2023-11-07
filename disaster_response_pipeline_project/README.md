# Disaster Response Pipeline Project
Within this project we process a data set containing real messages that were sent during disaster events. We creat a machine learning pipeline to categorize these events so that one can send the messages to an appropriate disaster relief agency.
The project includes a web app where an emergency worker can input a new message and get classification results in several categories. The web app also displays some visualizations of the data like about the different message types and the distribution of the most common categories. 


## Data
Within the data folder following files are provided and used for data mining and the build of the model.
| File         | Content | 
|--------------|:-----:|
|[disaster_messages.csv](data/disaster_messages.csv) | real messages that were sent during disaster events | 
| [disaster_categories.csv](data/disaster_categories.csv) |categories to which messages have been assigned |

## Dependencies
All the used python libs and their respective versions are listed in [requirements.txt](requirements.txt)

## Data Preparation
The preparation of the data has been performed with [ETL Pipeline Preparation.ipynb](ETL%20Pipeline%20Preparation.ipynb). The resulting code went into the script [process_data.py](data/process_data.py)

## Approaches for creating models
### 1. Standard
The original approach for constructing the model for the classification is based on TfidfVectorizer as featurizer and RandomForestClassifier. 
Notebook for this is [ML Pipeline Preparation.ipynb](ML%20Pipeline%20Preparation.ipynb). Within this notebook also some hyperparameter tuning via gridsearch has been performed. The final model construction logic went into the script [train_classifier.py](models/train_classifier.py)
### 2. Use bert-base-uncased transformer model
Here I used pretrained English model. As in the standard it was trained on the "message" attribute of the data. Notebook for the this approaches is [ML Pipeline Preparation - transformer.ipynb](ML%20Pipeline%20Preparation%20-%20transformer.ipynb)
### 3. Use bert-base-multilingual-cased model
As above, a pre trained model has been used. However this time it is a multinlingual one. In addition to this I also included the "original" attribute to the training data. This way, I got some sixteen thousand more data rows to train on. 
Notebook for that approache is also [ML Pipeline Preparation - transformer.ipynb](ML%20Pipeline%20Preparation%20-%20transformer.ipynb)




 
## Instructions:
#### Build the model
1. Run the following commands in the project's root directory to set up your database and model.
* Run ETL pipeline that cleans data and stores in database \
```
python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db
```
* Run ML pipeline that trains classifier and saves
        
```
python models/train_classifier.py data/DisasterResponse.db models/classifier.pkl
```
    

2. Run the following command in the **app**'s directory to run your web app.
    
```
python run.py
```

3. Go to http://0.0.0.0:3001/


## Outlook
It took a long time to implement and train the transformer based models. The results were not (yet) justifying this. However it would be nice to spend more effort here and experiment with transformer approach as I only scratched the surface of it. One  advantage I see hear, is the potential high model quality. With the usage of multi-lingual pretrained models it would also no longer be needed to first translate message data before classifying.