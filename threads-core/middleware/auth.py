from functools import wraps
import jwt
from flask import request, abort
from flask import current_app as app
from bson.objectid import ObjectId

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        try:
            data=jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            client = app.config['MONGO_CLIENT']
            db = client.get_database('threads')
            users_collection = db.get_collection('users')

            current_user = users_collection.find_one({'_id': ObjectId(data["user_id"])})
            if current_user is None:
                return {
                "message": "Invalid Authentication token!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        except Exception as e:
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }, 500

        return f(current_user, *args, **kwargs)

    return decorated