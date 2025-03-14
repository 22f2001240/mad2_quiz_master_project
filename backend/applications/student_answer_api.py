from flask import current_app as app,request
from flask_restful import Resource
from flask_jwt_extended import jwt_required,get_jwt_identity
from datetime import datetime
from .model import *
from .home import *

class StudentAnswerAPI(Resource):
    @jwt_required()
    @cache.cached(timeout=120)
    def get(self,score_id):
        user_id = get_jwt_identity()
        student_answers = StudentAnswer.query.filter_by(user_id = user_id,score_id=score_id).all() 
        if not student_answers:
            return {"message" : "You are not yet participated in any contests!!"}, 404
        student_answers_json = []
        for answer in student_answers:
            student_answers_json.append(answer.convert_to_json())
        return student_answers_json,200
    