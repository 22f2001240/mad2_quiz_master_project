from flask import current_app as app,request
from flask_restful import Resource
from flask_jwt_extended import jwt_required,get_jwt_identity
from datetime import datetime
from .model import *
from .home import *

class ScoresAPI(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        scores = Scores.query.filter_by(user_id = user_id).all() 
        if not scores:
            return {"message" : "You are not yet participated in any contests!!"}, 404
        scores_json = []
        for score in scores:
            scores_json.append(score.convert_to_json())
        return scores_json,200
    
    @jwt_required()
    def post(self,quiz_id):
        user_id = get_jwt_identity()
        data = request.json
        required_fields = ["total_score", "total_attempted_questions", "total_correct_answers", "total_wrong_answers"]
        if not all(field in data and data[field] for field in required_fields):
            return {"message" : 'Bad request! All fields are required.'},400
        # score = Scores.query.filter_by(user_id = user_id,quiz_id = quiz_id).first()
        # if score:
        #     return {"message" : "You have already participated in this quiz"}, 409
        new_score = Scores(total_score=data.get("total_score"),total_attempted_questions=data.get("total_attempted_questions"),total_correct_answers=data.get("total_correct_answers"),total_wrong_answers=data.get("total_wrong_answers"),user_id=user_id,quiz_id=quiz_id)
        db.session.add(new_score)
        db.session.commit()
        return {"message" : "Your score recorded successfully"},201
    