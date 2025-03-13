from flask import current_app as app,request
from flask_restful import Resource
from flask_jwt_extended import jwt_required,get_jwt
from functools import wraps
from flask_caching import Cache

cache=Cache()

class HomeAPI(Resource):
    def get(self):
        return {"message" : "This is the home page"}
    
def role_required(required_role):
    def decorator(func):
        @wraps(func)
        @jwt_required()
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            user_role = claims.get("role")
            if user_role not in required_role:
                return {"message" :"Unauthorized access!"}, 403
            return func(*args, **kwargs)
        return wrapper
    return decorator