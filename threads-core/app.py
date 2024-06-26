from flask import Flask, request
from flask_restful import Api, Resource
from api.routes import add_routes
from dotenv import load_dotenv
from pymongo import MongoClient
from celery import Celery
import os

load_dotenv()

def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=os.getenv('CELERY_BROKER_URL')
    )
    celery.conf.update(app.config)
    return celery

app = Flask(__name__)
api = Api(app)

app.config['DEBUG'] = True
client = MongoClient(os.getenv('MONGODB_URI'))
app.config['MONGO_CLIENT'] = client

celery = make_celery(app)
app.config['CELERY'] = celery

add_routes(api)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)