from flask import current_app as app,request
from flask_restful import Resource
from .model import *
from .home import *

class UserAPI(Resource):
    @jwt_required()
    @cache.cached(timeout=10)
    def get(self):
        users = User.query.filter_by(role='user').all() 
        user_json = []
        for user in users:
            user_json.append(user.convert_to_json())
        return user_json,200