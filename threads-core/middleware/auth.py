from functools import wraps
import jwt
from flask import request, abort, jsonify, make_response
from flask import current_app as app, g
from bson.objectid import ObjectId

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            token = None
            if "Authorization" in request.headers:
                token = request.headers["Authorization"].split(" ")[1]
            if not token:
                response_data = {
                    "message": "Authentication Token is missing!",
                    "data": None,
                    "error": "Unauthorized"
                }
                return make_response(jsonify(response_data), 401)

        
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            client = app.config['MONGO_CLIENT']
            db = client.get_database('threads')
            users_collection = db.get_collection('users')

            current_user = users_collection.find_one({'_id': ObjectId(data["user_id"])})
            if current_user is None:
                response_data = {
                    "message": "Invalid Authentication token!",
                    "data": None,
                    "error": "Unauthorized"
                }
                return make_response(jsonify(response_data), 401)

            # Add current_user to the request context
            g.current_user_id = data["user_id"]
        except Exception as e:
            import traceback
            traceback.print_exc()
            response_data = {
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }
            return make_response(jsonify(response_data), 500)

        return f(*args, **kwargs)

    return decorated
