from flask import current_app as app,request
from flask_restful import Resource
from flask_jwt_extended import jwt_required,get_jwt_identity
from datetime import datetime
from .model import *
from .home import *
from .task import notify_new_quiz,data_export

class QuizAPI(Resource):
    @jwt_required()
    @cache.cached(timeout=120)
    def get(self):
        quizzess = Quiz.query.all()
        quiz_json = []
        for quiz in quizzess:
            quiz_json.append(quiz.convert_to_json())
        return quiz_json,200
    
    @jwt_required()
    @role_required('admin')
    def post(self):
        data = request.json
        required_fields = ["name", "level", "date_of_quiz","chapter_id"]
        if not all(field in data and data[field] for field in required_fields):
            return {"message" : data['level']},400
        name, level, date_of_quiz_str, time_of_quiz_str, time_duration_str, remarks, chapter_id = data.get("name"), data.get("level"), data.get("date_of_quiz"), data.get("time_of_quiz"), data.get("time_duration"), data.get("remarks"), data.get("chapter_id")
        if len(name) <2 :
            return {"message" : "Name is too short. "},400
        if level not in ["Beginner","Intermediate","Advanced"]:
            return {"message" : "level should be any of these:Beginner,Intermediate,Advanced"},400
        date_of_quiz = datetime.strptime(date_of_quiz_str,"%Y-%m-%d").date()
        time_of_quiz_str = f"{time_of_quiz_str}:00"
        time_of_quiz = datetime.strptime(time_of_quiz_str, "%H:%M:%S").time() 
        time_duration = datetime.strptime(time_duration_str, "%H:%M").time()
        today = date.today()
        if date_of_quiz < today:
            return {"message": "Invalid date! Cannot use previous dates"}, 400
        quiz = Quiz.query.filter_by(name =name, chapter_id = chapter_id).first()
        if quiz:
            return {"message" : "Quiz already exist!"},409 
        new_quiz = Quiz(name = name, level=level, date_of_quiz = date_of_quiz, time_of_quiz = time_of_quiz, time_duration = time_duration, remarks = remarks, chapter_id = chapter_id)
        db.session.add(new_quiz)
        db.session.commit()
        notify_new_quiz.delay(new_quiz.name)
        cache.clear()
        return {"message" : "New Quiz created successfully","quiz_id":new_quiz.id},201
    
    @jwt_required()
    @role_required('admin')
    def put(self,quiz_id):
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return {"message" : "Quiz doest not found"}, 404
        data = request.json
        quiz.name = data.get("name") if data.get("name") else quiz.name
        quiz.level = data.get("level") if data.get("level") else quiz.level
        if data.get("date_of_quiz"):
            date_of_quiz_str = data.get("date_of_quiz")
            date_of_quiz = datetime.strptime(date_of_quiz_str,"%Y-%m-%d").date()
            # date_of_quiz = datetime.strptime(date_of_quiz_str,"%d-%m-%Y").date()
            today = date.today()
            if date_of_quiz < today:
                return {"message": "Invalid date! Cannot use previous dates"}, 400
            quiz.date_of_quiz = date_of_quiz
        else:
            quiz.date_of_quiz = quiz.date_of_quiz
        if data.get("time_of_quiz"):
            time_of_quiz_str = data.get("time_of_quiz")
            time_of_quiz_str = f"{time_of_quiz_str}:00"
            # time_of_quiz_str = time_of_quiz_str
            time_of_quiz = datetime.strptime(time_of_quiz_str,"%H:%M:%S").time()
            quiz.time_of_quiz = time_of_quiz
        else:
            quiz.time_of_quiz = quiz.time_of_quiz
        if data.get("time_duration"):
            time_duration_str = data.get("time_duration")
            time_duration = datetime.strptime(time_duration_str,"%H:%M").time()
            quiz.time_duration = time_duration
        else:
            quiz.time_duration = quiz.time_duration
        quiz.remarks = data.get("remarks") if data.get("remarks") else quiz.remarks
        quiz.chapter_id = data.get("chapter_id") if data.get("chapter_id") else quiz.chapter_id
        db.session.commit()
        cache.clear()
        return {"message" : "Quiz updated successfully"},200
    
    @jwt_required()
    @role_required('admin')
    def delete(self,quiz_id):
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return {"message" : "Quiz doest not found"}, 404
        db.session.delete(quiz)
        db.session.commit()
        cache.clear()
        return {"message" : "Requested quiz deleted succesfully"}, 200

class OneQuizAPI(Resource):
    @jwt_required()
    @cache.cached(timeout=120)
    def get(self,chapter_id):
        quizzes = Quiz.query.filter_by(chapter_id = chapter_id).all()
        if not quizzes:
            return {"message" : "Quiz doest not found for the chapter"}, 404
        quiz_json = []
        for quiz in quizzes:
            quiz_json.append(quiz.convert_to_json())
        return quiz_json,200

class SingleQuizAPI(Resource):
    @jwt_required()
    @cache.cached(timeout=120)
    def get(self,quiz_id):
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return {"message" : "Quiz doest not found "}, 404
        return quiz.convert_to_json(),200

#get for fetching completed quizzes from student dashboad 
class CompletedQuizessStudentAPI(Resource):
    @jwt_required()
    @cache.cached(timeout=120)
    def get(self):
        user_id = get_jwt_identity()
        scores = Scores.query.filter_by(user_id=user_id)
        if not scores:
            return {"message" : "You are not yet participated in any quizzes"}
        quiz_json = []
        for score in scores:
            quiz = Quiz.query.get(score.quiz_id)
            quiz_json.append(quiz.convert_to_json())
        return quiz_json
            

class ExportDataAPI(Resource):
    @jwt_required()
    @cache.cached(timeout=120)
    def get(self):
        scores = Scores.query.all()
        quiz_details = []
        for score in scores:
            quiz = Quiz.query.get(score.quiz_id)
            quiz_details.append({'quiz_id':quiz.id, 'chapter_name':quiz.chapter.name, 'level':quiz.level, 'date_of_quiz':quiz.date_of_quiz, 'time_of_quiz':quiz.time_of_quiz, 'time_duration':quiz.time_duration,'reamrks':quiz.remarks})
        data_export(quiz_details)
        return {"message":"Data export task has been initiated, Please check your inbox"},200
    


