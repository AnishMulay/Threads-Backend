from flask import Flask, request
from flask_restful import Api, Resource
from api.routes import add_routes
from dotenv import load_dotenv
from pymongo import MongoClient
import os

load_dotenv()

app = Flask(__name__)
api = Api(app)

app.config['DEBUG'] = True
client = MongoClient(os.getenv('MONGODB_URI'))
app.config['MONGO_CLIENT'] = client

add_routes(api)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)