from flask_sqlalchemy import SQLAlchemy
from datetime import date,time
from sqlalchemy.sql import func

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key = True)
    role = db.Column(db.String, nullable = False, default = 'user') #['admin', 'user]
    email = db.Column(db.String, unique = True, nullable = False)
    password = db.Column(db.String(20), nullable = False)
    name = db.Column(db.String(20), nullable = False)
    qualification = db.Column(db.String(20), default = 'Beginner') #['Beginner', 'Intermediate', 'Advanced']
    dob = db.Column(db.Date)
    interested_subjects = db.Column(db.Integer, db.ForeignKey("subject.id"))
    reminder_time = db.Column(db.Time, default=time(17, 0, 0)) #default time for sending reminders is 5 pm

class Subject(db.Model):
    __tablename__ = 'subject'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False, unique = True)
    description = db.Column(db.String)

class Chapter(db.Model):
    __tablename__ = 'chapter'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    description = db.Column(db.String)
    subject_id = db.Column(db.Integer, db.ForeignKey("subject.id"), nullable = False)

class Quiz(db.Model):
    __tablename__ = 'quiz'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    chapter_id = db.Column(db.Integer, db.ForeignKey("chapter.id"), nullable = False)
    level = db.Column(db.String, nullable = False) #['Beginner', 'Intermediate', 'Advanced']
    date_of_quiz = db.Column(db.Date, nullable = False)
    time_duration = db.Column(db.Time, nullable = False, default = time(1,00)) # format - hh:mm - 01:00
    remarks = db.Column(db.String)
    top_score = db.Column(db.Integer, db.ForeignKey("scores.id"))

class Questions(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key = True)
    question = db.Column(db.String, nullable = False)
    option_a = db.Column(db.String, nullable = False)
    option_b = db.Column(db.String, nullable = False)
    option_c = db.Column(db.String, nullable = False)
    option_d = db.Column(db.String, nullable = False)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id"), nullable = False)
    correct_option = db.Column(db.String, nullable = False)
    mark = db.Column(db.Integer, nullable = False)

class Scores(db.Model):
    __tablename__ = 'scores'
    id = db.Column(db.Integer, primary_key = True)
    total_score = db.Column(db.Integer, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id"), nullable = False)
    submitted_at = db.Column(db.DateTime, nullable=False, default=func.now())
    total_attempted_questions = db.Column(db.Integer, nullable = False)
    total_correct_answers = db.Column(db.Integer, nullable = False)
    total_wrong_answers = db.Column(db.Integer, nullable = False)


