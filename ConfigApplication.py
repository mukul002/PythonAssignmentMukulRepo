from flask import Flask, jsonify
from pymongo import MongoClient
import configparser
import os
import certifi

app = Flask(__name__)

client = MongoClient("mongodb+srv://admin:Admin1234@cluster0.9sniusr.mongodb.net/",
                     tlsCAFile=certifi.where())
db = client["mynewdb"]
config_collection = db["configurations"]

def read_config(file_path="config.ini"):
    config = configparser.ConfigParser()
    data = {}

    if not os.path.exists(file_path):
        return None 

    config.read(file_path)

    for section in config.sections():
        data[section] = {}
        for key, value in config.items(section):
            data[section][key] = value
    return data

@app.route("/")
def home():
    return "Hello, User! Config Manager is running"

@app.route("/load_config")
def load_config():
    # Read config from file
    config_data = read_config()
    if not config_data:
        return jsonify({"error": "Config file not found!"}), 404

    # Clear previous configs and insert new one
    config_collection.delete_many({})
    result = config_collection.insert_one(config_data)

    response_data = {
        "message": "Config loaded into DB!",
        "inserted_id": str(result.inserted_id)
    }

    return jsonify(response_data)


@app.route("/config")
def get_config():
    config_data = config_collection.find_one({}, {"_id": 0}) 
    if not config_data:
        return jsonify({"error": "No config found in DB"}), 404
    return jsonify(config_data)

if __name__ == "__main__":
    app.run(debug=False)
