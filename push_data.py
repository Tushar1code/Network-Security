import os
import sys
import json
import certifi
import pandas as pd
import pymongo
from dotenv import load_dotenv
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

# Load environment variables
load_dotenv()

# Make sure the variable name matches .env
MONGO_DB_URI = os.getenv("MONGO_DB_URI")
if not MONGO_DB_URI:
    raise ValueError("MongoDB URI not found in environment variables. Please check your .env file.")

ca = certifi.where()

class NetworkDataExtract:
    def __init__(self):
        pass
        
    def csv_to_json_convertor(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def insert_data_mongodb(self, records, database, collection):
        try:
            mongo_client = pymongo.MongoClient(MONGO_DB_URI, tlsCAFile=ca)
            db = mongo_client[database]
            coll = db[collection]
            coll.insert_many(records)
            return len(records)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
if __name__ == '__main__':
    FILE_PATH = r"Network_Data/phisingData.csv"  # fixed path issue
    DATABASE = "KRISHAI"
    COLLECTION = "NetworkData"

    networkobj = NetworkDataExtract()
    
    # Convert CSV to JSON
    records = networkobj.csv_to_json_convertor(file_path=FILE_PATH)
    logging.info(f"Total records found in CSV: {len(records)}")

    # Insert into MongoDB
    no_of_records = networkobj.insert_data_mongodb(records, DATABASE, COLLECTION)
    logging.info(f"Inserted {no_of_records} records into MongoDB.")
    print(f"Inserted {no_of_records} records into MongoDB.")
