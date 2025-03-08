from flask import current_app as app,request
from flask_restful import Resource
from .model import *
from .home import *

class QuestionsAPI(Resource):
    @jwt_required()
    def get(self):
        questions = Questions.query.all()
        questions_json = []
        for question in questions:
            questions_json.append(question.convert_to_json())
        return questions_json,200

    @jwt_required()
    @role_required('admin')
    def post(self):
        data = request.json
        required_fields = ["question", "option_a", "option_b","option_c", "option_d", "correct_option", "mark", "quiz_id"]
        if not all(field in data and data[field] for field in required_fields):
            return {"message" : 'Bad request! All fields are required.'},400
        question, option_a, option_b,option_c, option_d, correct_option, mark, quiz_id = data.get("question"),data.get("option_a"), data.get("option_b"),data.get("option_c"),data.get("option_d"),data.get("correct_option"),data.get("mark"),data.get("quiz_id")
        if len(question) <5 :
            return {"message" : "Question is too short. "},400
        if mark <= 0 :
            return {"message" : "Mark should be greater than 0"},400
        if correct_option not in ['option_a', 'option_b','option_c', 'option_d']:
            return {"message" : "Options should be any of this : option_a, option_b,option_c, option_d"},400
        quest = Questions.query.filter_by(question = question, quiz_id = quiz_id).first()
        if quest:
            return {"message" : "Question already exist!"},409
        new_question = Questions(question = question, option_a = option_a, option_b = option_b,option_c = option_c, option_d = option_d, correct_option = correct_option, mark = mark, quiz_id = quiz_id)
        db.session.add(new_question)
        db.session.commit()
        return {"message" : "New question created successfully"},201
    
    @jwt_required()
    @role_required('admin')
    def put(self,question_id):
        quest = Questions.query.get(question_id)
        if not quest:
            return {"message" : "Question not found"}, 404
        data = request.json
        if data.get("mark") and data.get("mark")<=0:
            return {"message" : "Mark should be greater than 0"},400
        if data.get("correct_option") and data.get("correct_option") not in ['option_a', 'option_b','option_c', 'option_d']:
            return {"message" : "Options should be any of this : option_a, option_b,option_c, option_d"},400
        quest.question = data.get("question") if data.get("question") else quest.question
        quest.option_a = data.get("option_a") if data.get("option_a") else quest.option_a
        quest.option_b = data.get("option_b") if data.get("option_b") else quest.option_b
        quest.option_c = data.get("option_c") if data.get("option_c") else quest.option_c
        quest.option_d = data.get("option_d") if data.get("option_d") else quest.option_d
        quest.correct_option = data.get("correct_option") if data.get("correct_option") else quest.correct_option
        quest.mark = data.get("mark") if data.get("mark") else quest.mark
        quest.quiz_id = data.get("quiz_id") if data.get("quiz_id") else quest.quiz_id
        db.session.commit()
        return {"message" : "Question updated successfully"},200
    
    @jwt_required()
    @role_required('admin')
    def delete(self,question_id):
        quest = Questions.query.get(question_id)
        if not quest:
            return {"message" : "Question not found"}, 404
        db.session.delete(quest)
        db.session.commit()
        return {"message" : "Question deleted succesfully"}, 200
    
class QuizQuestionsAPI(Resource):
    @jwt_required()
    def get(self,quiz_id):
        questions = Questions.query.filter_by(quiz_id = quiz_id).all()
        if not questions:
            return {"message" : "Question set doest not found"}, 404
        questions_json = []
        for question in questions:
            questions_json.append(question.convert_to_json())
        return {"data":questions_json, "quiz_id" : quiz_id},200
    
class SingleQuestionAPI(Resource):
    @jwt_required()
    def get(self,question_id):
        question = Questions.query.get(question_id)
        if not question:
            return {"message" : "Question doest not found"}, 404
        return question.convert_to_json(),200



     
