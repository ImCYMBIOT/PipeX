import pandas as pd
import boto3
from sqlalchemy import create_engine
from pymongo import MongoClient

def load_data(target: str, config: dict, data: pd.DataFrame):
    if target == "s3":
        s3 = boto3.client(
            "s3",
            aws_access_key_id=config["aws_access_key_id"],
            aws_secret_access_key=config["aws_secret_access_key"],
            region_name=config["region_name"]
        )
        
        csv_buffer = data.to_csv(index=False)
        s3.put_object(Bucket=config['bucket_name'], Key=config['file_name'], Body=csv_buffer)
        print(f"Data loaded to S3 bucket: {config['bucket_name']}")

    elif target == "database":
        db_type = config.get("db_type")
        if db_type == "mysql":
            engine = create_engine(
                f"mysql+mysqlconnector://{config['username']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"
            )
        elif db_type == "postgres":
            engine = create_engine(
                f"postgresql+psycopg2://{config['username']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"
            )
        else:
            raise ValueError("Database type not supported.")
        
        data.to_sql(config['table_name'], engine, if_exists='replace', index=False)
        print(f"Data loaded to {db_type} database: {config['database']}")

    elif target == "non_relational_database":
        db_type = config.get("db_type")
        if db_type == "mongodb":
            client = MongoClient(
                host=config["host"],
                port=config["port"],
                username=config["username"],
                password=config["password"]
            )
            db = client[config["database"]]
            collection = db[config["collection"]]
            collection.insert_many(data.to_dict("records"))
            print(f"Data loaded to MongoDB collection: {config['collection']}")
            client.close()
        else:
            raise ValueError("Non-relational database type not supported.")

    elif target == "file":
        file_type = config.get("file_type")
        if file_type == "csv":
            data.to_csv(config['file_path'], index=False)
            print(f"Data loaded to CSV file: {config['file_path']}")
        elif file_type == "json":
            data.to_json(config['file_path'], orient='records', lines=True)
            print(f"Data loaded to JSON file: {config['file_path']}")
        else:
            raise ValueError("File type not supported.")
    else:
        raise ValueError("Target type not supported.")