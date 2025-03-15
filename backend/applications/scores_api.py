from flask import current_app as app,request
from flask_restful import Resource
from flask_jwt_extended import jwt_required,get_jwt_identity
from datetime import datetime
from .model import *
from .home import *

class ScoresAPI(Resource):
    @jwt_required()
    @cache.cached(timeout=120)
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
        submitted_score = data.get("scores")
        question_answers = data.get("question_answers")
        required_fields = ["total_score", "total_attempted_questions", "total_correct_answers", "total_wrong_answers"]
        if not all(field in submitted_score and submitted_score[field] for field in required_fields):
            return {"message" : 'Bad request! All fields are required.'},400
        score = Scores.query.filter_by(user_id = user_id,quiz_id = quiz_id).first()
        if score:
            return {"message" : "You have already participated in this quiz"}, 409
        new_score = Scores(total_score=submitted_score["total_score"],total_attempted_questions=submitted_score["total_attempted_questions"],total_correct_answers=submitted_score["total_correct_answers"],total_wrong_answers=submitted_score["total_wrong_answers"],user_id=user_id,quiz_id=quiz_id)
        db.session.add(new_score)
        db.session.commit()
        score_id = new_score.id
        for item in question_answers:
            new_student_answer = StudentAnswer(selected_option = item['selected_option'], question_id = item['question_id'],user_id = user_id, score_id = score_id)
            db.session.add(new_student_answer)
        db.session.commit()
        cache.clear()
        return {"message" : "Your score recorded successfully"},201
    
#For Admin Summary
class SubjectTopScoreAPI(Resource):
    @jwt_required()
    def get(self):
        scores = Scores.query.all()
        if scores == []:
            return {"message" : 'Nobody attempted any of the quizzes'},404
        subject_top_score = {}
        for score in scores:
            if score.quiz.chapter.subject.name not in subject_top_score:
                subject_top_score[score.quiz.chapter.subject.name] = score.total_score
            elif subject_top_score[score.quiz.chapter.subject.name] < score.total_score:
                subject_top_score[score.quiz.chapter.subject.name] = score.total_score
        return subject_top_score,200   
    
class SubjectUserAttemptAPI(Resource):
    @jwt_required()
    def get(self):
        scores = Scores.query.all()
        if scores == []:
            return {"message" : 'Nobody attempted any of the quizzes'},404
        subject_user_attempt = {}
        for score in scores:
            if score.quiz.chapter.subject.name not in subject_user_attempt:
                subject_user_attempt[score.quiz.chapter.subject.name] = 1
            else:
                subject_user_attempt[score.quiz.chapter.subject.name] += 1
        return subject_user_attempt,200

#For Student Summary
class SubjectNumQuizzesAPI(Resource):
    @jwt_required()
    def get(self):
        quizzes = Quiz.query.all()
        if not quizzes:
            return {"message" : "No Quizzes are Available now"}, 404
        subject_quizzes = {}
        for quiz in quizzes:
            if quiz.chapter.subject.name not in subject_quizzes:
                subject_quizzes[quiz.chapter.subject.name] = 1
            else : 
                subject_quizzes[quiz.chapter.subject.name] += 1
        return subject_quizzes,200

class SubjectAttemptAPI(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        scores = Scores.query.filter_by(user_id=user_id).all()
        if scores == []:
            return {"message" : 'You are Not Attempted Any Quizzes Yet!'},404
        subject_attempt = {}
        for score in scores:
            if score.quiz.chapter.subject.name not in subject_attempt:
                subject_attempt[score.quiz.chapter.subject.name] = 1
            else:
                subject_attempt[score.quiz.chapter.subject.name] += 1
        return subject_attempt,200
