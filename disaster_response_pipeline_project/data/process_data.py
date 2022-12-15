import sys
import logging
import pandas as pd
from sqlalchemy import create_engine


logger = logging.getLogger()


def load_data(messages_filepath, categories_filepath):
    ''' loads data from csv files

    INPUT:
        messages_filepath   - path to messages dataset csv filea
        categories_filepath - path to categories dataset csv file

    OUTPUT:
        df_msg, df_cat      - tuple of pandas dataframes
    '''
    try:
        df_msg = pd.read_csv(messages_filepath)
        df_cat = pd.read_csv(categories_filepath, sep=',')
    except Exception as exception:
        logger.error(
            f'could not read data files ({messages_filepath}, {categories_filepath}). {exception}')
        return None
    return df_msg, df_cat


def clean_data(df_msg, df_cat):
    ''' cleans and merges the data

    INPUT:
        df_msg, df_cat - tuple of pandas dataframes containing message and category data

    OUTPUT:
        df_clean       - dataframe containing merged and cleaned data
    '''
    logger.info(f'clean_data with input messages shape {df_msg.shape} \
        and categories shape {df_cat.shape}')
    ###########################################################################
    ###### split categories into separate cols START ##########################
    ###########################################################################
    df_cat = pd.concat([df_cat['id'],
                        df_cat['categories'].str.split(pat=';', n=-1, expand=True)],
                       axis=1, join='inner')
    # get only the category columns
    cat_cols = df_cat[df_cat.columns[1:]]
    # create new headers from first row
    row = cat_cols.head(1).values[0]
    category_colnames = [name[:-2] for name in row]
    new_header_names = ['id']
    new_header_names.extend(category_colnames)
    # rename the columns of `categories`
    df_cat.columns = new_header_names
    ###########################################################################
    ###### split categories into separate cols END ############################
    ###########################################################################

    ###########################################################################
    ###### convert category values to numbers START ###########################
    ###########################################################################
    for column in df_cat[df_cat.columns[1:]]:
        # set each value to be the last character of the string
        df_cat[column] = df_cat[column].astype(str).str[-1]
        # convert column from string to numeric
        df_cat[column] = df_cat[column].astype(int)
        # allow only values 0 and 1
        df_cat[column] = df_cat[column].apply(lambda x: 0 if x == 0 else 1 )
    ###########################################################################
    ###### convert category values to numbers END #############################
    ###########################################################################

    # concatenate df_msg, df_cat
    df = pd.merge(df_msg, df_cat, on=['id'])
    logger.info(f'merged dataset has shape {df.shape}')

    # remove duplicates
    df.drop_duplicates(inplace=True)
    logger.info(f'merged dataset shape after duplicates removal {df.shape}')

    return df


def save_data(df, database_filename):
    ''' saves dataframe into sql-lite db

    INPUT:
        df                  - dataframe to be stored in db
        database_filename   - path to db store

    OUTPUT:
        boolean             - true if df successfully stored into db
    '''
    try:
        engine = create_engine(f'sqlite:///{database_filename}')
        df.to_sql('CleanedData', engine, index=False)
        logger.info(
            f'successfully stored df (shape {df.shape}) into sql db {database_filename}).')
    except Exception as exception:
        logger.error(
            f'could not store df (shape {df.shape}) to sql db {database_filename}). {exception}')
        return False
    return True


def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df_msg, df_cat = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df_msg, df_cat)

        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)

        print('Cleaned data saved to database!')

    else:
        print('Please provide the filepaths of the messages and categories '
              'datasets as the first and second argument respectively, as '
              'well as the filepath of the database to save the cleaned data '
              'to as the third argument. \n\nExample: python process_data.py '
              'disaster_messages.csv disaster_categories.csv '
              'DisasterResponse.db')


if __name__ == '__main__':
    main()
