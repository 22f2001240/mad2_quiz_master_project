from flask import current_app as app,request
from flask_restful import Resource

class HomeAPI(Resource):
    def get(self):
        return {"message" : "This is the home page"}