# Sparkify Project

Goal of this project is to use a large and realistic datasets with Spark to engineer relevant features for predicting churn. The data comes from a virtual digital data stream provider similar to Spotify, Tidel or Amazon Music.
We want to use this data to create an ML model which will allow us users who are about to quit our service before they actual leave. This will allow the business to offer them discounts or other special offers.

### Essential Skills
Essential skill shown in this project are:
* Load large datasets into Spark and manipulate them using Spark SQL and Spark Dataframes
* Use the machine learning APIs within Spark ML to build and tune models

## Dependencies
All the used python libs and their respective versions are listed in [requirements.txt](requirements.txt)

## Data
The dataset used for this project is quite large and thus not itsself included inside this repository but can be downloaded [here](https://55acordkzr.prod.udacity-student-workspaces.com/edit/mini_sparkify_event_data.json).

### Schema
The data consists of rows containing timestamped entries with user and event related attributes.
```
root
 |-- artist: string (nullable = true)
 |-- auth: string (nullable = true)
 |-- firstName: string (nullable = true)
 |-- gender: string (nullable = true)
 |-- itemInSession: long (nullable = true)
 |-- lastName: string (nullable = true)
 |-- length: double (nullable = true)
 |-- level: string (nullable = true)
 |-- location: string (nullable = true)
 |-- method: string (nullable = true)
 |-- page: string (nullable = true)
 |-- registration: long (nullable = true)
 |-- sessionId: long (nullable = true)
 |-- song: string (nullable = true)
 |-- status: long (nullable = true)
 |-- ts: long (nullable = true)
 |-- userAgent: string (nullable = true)
 |-- userId: string (nullable = true)
```

We will use some of these attributes as well as additionally created features as input for the trainings of our models.

## Approach
The following steps have been performed to get from the data to the best performing model:
* Load and Clean Dataset: We loaded the data and removed rows which were not complete in attributes minimally needed for our analysis and later steps.
* Exploratory Data Analysis: We had a more detailed look into the data to identify promissing attributes for our evaluation. We also added additional attributes describing downgrades, churnes and also user lifecycle phases.
* Feature Engineering: We created some categorical features, features describung numeric values per user and also features per user and day timestamps.
* Modeling: We split the data into train and test sets and used this to train and evaluate several different models.

All the details and outcomes of this are document within a [Jupyter notebook](Sparkify.ipynb)


## Instructions:
* Create a virtual Python environment based on the [requirements.txt](requirements.txt)
* Execute the [Jupyter notebook](Sparkify.ipynb)

## Reference:
[Blogpost](blogpost.md) of this project.

## Licencing
[Creative Commons Legal Code](LICENSE)