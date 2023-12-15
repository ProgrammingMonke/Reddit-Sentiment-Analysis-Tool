from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from typing import List
from dotenv import dotenv_values
import reddit_scraper
import random

secrets = dotenv_values(".env")

# Change it so that username and password is passed in
def connect_to_db():
    """
    Attempts to connect to mongodb cluster
    """
    uri = "mongodb+srv://" + secrets["DB_USERNAME"] + ":" + secrets["DB_PASSWORD"] + "@cluster0.wgtehoy.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri, server_api=ServerApi('1'))

    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
        return -1

    return client['labeled_titles']

def upload_title(db, label: int, title: str) -> int:
    """
    Uploads titles and label to database

    :param db: database that the data is going to uploaded to
    :param label: label that corresponds with the title
    :param title: Reddit title that is being classified
    :return: 0 for success, 1 for failure
    """ 
    collection = db['labeled_titles']

    if collection.find_one({"title": title}):
        print("Title already in database")
        return 1

    # Upload a title with the corresponding label to the specified category
    try:
        collection.insert_one({"label": label, "title": title})
        return 0
    except Exception as e:
        print(f"Error uploading title: {e}")
        return 1

def remove_title(db, title: str) -> int:
    """
    Uploads titles and label to database

    :param db: database that the data is going to uploaded to
    :param title: Reddit title that needs to be deleted
    :return: 0 for success, 1 for failure
    """ 
    collection = db['labeled_titles']

    # Remove a title from the database based on the title string
    try:
        result = collection.delete_one({"title": title})
        if result.deleted_count >= 1:
            return 0 
        else:
            return 1
    except Exception as e:
        print(f"Error removing title: {e}")
        return 1

def get_db_count(db) -> List[int]:
    """
    Returns count of each category in db

    :param db: database that the data is going to uploaded to
    :return: [israel_count, neutral_count, palestine_count]
    """ 
    collection = db['labeled_titles']

    # Count the number of titles in each category (Israel, Neutral, Palestine)
    israel_count = collection.count_documents({"label": -1})
    neutral_count = collection.count_documents({"label": 0})
    palestine_count = collection.count_documents({"label": 1})
    return [israel_count, neutral_count, palestine_count]

def get_titles(db):
    """
    Calls Reddit Scraper. Removes any titles already in the database.

    :param db: database that the data is going to uploaded to
    :return: unseen titles from subreddits
    """ 
    titles = reddit_scraper.get_titles()
    collection = db['labeled_titles']

    # Use list comprehension to filter out titles that already exist in the database
    return_titles = [title for title in titles if not collection.find_one({"title": title})]

    return return_titles

def get_database_content(db, training, testing, scramble):
    """
    Returns all the data within the mongodb server and splits it up into training
    and test data

    :param db: database that the data is going to uploaded to
    :param training: a number from 0-1 that specifies the amount of data needed for training
    :param testing: a number from 0-1 that specifies the amount of data needed for training
    :param scramble: if set to 1, split dataset randomly. If set to 0, training data will always be the first _% of database

    :return: all data within the collection split into two jsons (size of jsons based on input)
    """ 
    collection = db['labeled_titles']
    total_data = collection.find({}, {"title": 1, "label": 1, "_id": 0})
    total_data = list(total_data)

    if not 0 <= training <= 1:
        print(training)
        print("Training set must be between 0 and 1")
        return [{}]
    
    if not 0 <= testing <= 1:
        print("Testing set must be between 0 and 1")
        return [{}]
            
    if training + testing != 1:
        print("Testing and Training set must add together to equal 1")
        return [{}]
    
    if scramble:
        random.shuffle(total_data)

    split_index = int(len(total_data) * training)
    training_data = total_data[:split_index]
    testing_data = total_data[split_index:]

    return training_data, testing_data