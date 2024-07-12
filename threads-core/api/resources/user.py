from flask_restful import Resource
from flask import current_app as app,g
from flask import request, jsonify, make_response
import bcrypt
import jwt  
from bson.json_util import dumps
from middleware.auth import token_required 

class UserResource(Resource):
    def post(self):
        try:
            print("INSIDE REGISTER POST REQUEST")

            username = request.json.get('username')
            password = request.json.get('password')
            email = request.json.get('email')

            if not username or not password or not email:
                raise ValueError("Username, password, and email are required fields.")

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            client = app.config['MONGO_CLIENT']
            db = client.get_database('threads')
            users_collection = db.get_collection('users')

            if users_collection.find_one({'username': username}):
                raise ValueError("Username already exists.")
            if users_collection.find_one({'email': email}):
                raise ValueError("Email already exists.")

            user = {
                'username': username,
                'password': hashed_password,
                'email': email
            }

            result = users_collection.insert_one(user)

            if result.inserted_id:
                response_data = {
                    'message': 'User registered successfully',
                    'user_id': str(result.inserted_id)
                }
                return make_response(jsonify(response_data), 201)
            else:
                raise Exception('Failed to register user')

        except Exception as e:
            import traceback
            traceback.print_exc()
            response_data = {
                "error": str(e)
            }
            return make_response(jsonify(response_data), 500)
        
    @token_required
    def get(self):
        try:
            print("INSIDE GET USERS")
            current_user_id = g.current_user_id
            print("current user: ", current_user_id)
            client = app.config['MONGO_CLIENT']
            db = client.get_database('threads')
            users_collection = db.get_collection('users')
            users = users_collection.find({}, {"password": 0})  # Exclude password from response
            users_list = list(users)
            print("user: ", users_list[0])
            return make_response(dumps(users_list), 200)
        
        except Exception as e:
            import traceback
            traceback.print_exc()
            response_data = {
                "error": str(e)
            }
            return make_response(jsonify(response_data), 500)



class Login(Resource):
    def post(self):
        try:
            print("INSIDE LOGIN POST REQUEST")

            username = request.json.get('username')
            password = request.json.get('password')

            if not username or not password:
                raise ValueError("Username and password are required fields.")

            client = app.config['MONGO_CLIENT']
            db = client.get_database('threads')
            users_collection = db.get_collection('users')

            user = users_collection.find_one({'username': username})
            user
            if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
                user["token"] = jwt.encode(
                    {"user_id": str(user["_id"])},
                    app.config["SECRET_KEY"],
                    algorithm="HS256"
                )
                response_data = {
                    "message": "Successfully fetched auth token",
                    "data": user
                }
                return make_response(dumps(response_data), 200)
            
            else:
                raise ValueError("Invalid username or password")

        except Exception as e:
            import traceback
            traceback.print_exc()
            response_data = {
                "error": str(e)
            }
            return make_response(jsonify(response_data), 500)
