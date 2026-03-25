from dotenv import load_dotenv
import os
import yaml

load_dotenv()
BOT_KEY = os.getenv('BOT_KEY')
DB_PASSWORD = os.getenv('DB_PASSWORD')


with open('config.yaml', mode='r') as file:
    config = yaml.safe_load(file)


DB_CONFIG = {
    "host": config["database"]["host"],
    "port": config["database"]["port"],
    "database": config["database"]["database"],
    "user": config["database"]["user"],
    "password": DB_PASSWORD
}



