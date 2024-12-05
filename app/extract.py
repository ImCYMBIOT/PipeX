import requests
import pandas as pd
import mysql.connector
import psycopg2
from pymongo import MongoClient

def extract_data(source_type: str, connection_details: dict, query_or_endpoint: str):
    if source_type == "api":
        response = requests.get(query_or_endpoint, headers=connection_details.get("headers", {}))
        data = response.json()
        print("Data extracted from API!")
        return data

    elif source_type == "database":
        db_type = connection_details.get("db_type")
        if db_type == "mysql":
            connection = mysql.connector.connect(
                host=connection_details['host'],
                user=connection_details['user'],
                password=connection_details['password'],
                database=connection_details['database']
            )
        elif db_type == "postgres":
            connection = psycopg2.connect(
                host=connection_details['host'],
                user=connection_details['user'],
                password=connection_details['password'],
                database=connection_details['database']
            )
        else:
            raise ValueError("Database type not supported.")
        
        df = pd.read_sql(query_or_endpoint, connection)
        connection.close()
        print("Data extracted from database.")
        return df
    
    elif source_type == "non_relational_database":
        db_type = connection_details.get("db_type")
        if db_type == "mongodb":
            client = MongoClient(
                host=connection_details["host"],
                port=connection_details["port"],
                username=connection_details["username"],
                password=connection_details["password"]
            )
            db = client[connection_details["database"]]
            collection = db[connection_details["collection"]]
            data = list(collection.find(query_or_endpoint))
            client.close()
            print("Data extracted from MongoDB!")
            return data
        else:
            raise ValueError("Unsupported non-relational database type")

    elif source_type == "file":
        file_type = connection_details.get("file_type")
        if file_type == "csv":
            df = pd.read_csv(query_or_endpoint)
            print("Data extracted from CSV file.")
        elif file_type == "json":
            df = pd.read_json(query_or_endpoint)
            print("Data extracted from JSON file.")
        else:
            raise ValueError("File type not supported.")
        return df
    
    else:
        raise ValueError("Unsupported source type.")