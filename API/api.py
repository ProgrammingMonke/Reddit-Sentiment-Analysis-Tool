from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from typing import List
from dotenv import dotenv_values
import reddit_scraper

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

def get_titles():
    """
    Calls Reddit Scraper

    :return: 99 titles from subreddits
    """ 
    return reddit_scraper.get_titles()