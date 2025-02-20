from flask_sqlalchemy import SQLAlchemy
from datetime import date,time
from sqlalchemy.sql import func

db = SQLAlchemy()

# Association table for Many-to-Many relationship (user - subject)
user_subject = db.Table(
    'user_subject',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key = True),
    db.Column('subject_id', db.Integer, db.ForeignKey('subject.id'), primary_key = True)
)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key = True)
    role = db.Column(db.String, nullable = False, default = 'user') #['admin', 'user]
    email = db.Column(db.String, unique = True, nullable = False)
    password = db.Column(db.String(20), nullable = False)
    name = db.Column(db.String(20), nullable = False)
    qualification = db.Column(db.String(20), default = 'Beginner') #['Beginner', 'Intermediate', 'Advanced']
    dob = db.Column(db.Date)
    subjects = db.relationship("Subject", secondary = user_subject, backref = "users", lazy = True)
    reminder_time = db.Column(db.Time, default = time(17, 0, 0)) #default time for sending reminders is 5 pm
    scores = db.relationship("Scores", backref = "user", cascade = "all, delete", lazy = True)

class Subject(db.Model):
    __tablename__ = 'subject'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False, unique = True)
    description = db.Column(db.String)
    chapters = db.relationship("Chapter", backref = "subject", cascade = "all, delete", lazy = True)

class Chapter(db.Model):
    __tablename__ = 'chapter'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    description = db.Column(db.String)
    subject_id = db.Column(db.Integer, db.ForeignKey("subject.id"), nullable = False)
    quizzes = db.relationship("Quiz", backref = "chapter", cascade = "all, delete", lazy = True)

class Quiz(db.Model):
    __tablename__ = 'quiz'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    level = db.Column(db.String, nullable = False) #['Beginner', 'Intermediate', 'Advanced']
    date_of_quiz = db.Column(db.Date, nullable = False)
    time_duration = db.Column(db.Time, nullable = False, default = time(1,00)) # format - hh:mm - 01:00
    remarks = db.Column(db.String)
    chapter_id = db.Column(db.Integer, db.ForeignKey("chapter.id"), nullable = False)
    questions = db.relationship("Questions", backref = "quiz", cascade = "all, delete", lazy = True)
    scores = db.relationship("Scores", backref = "quiz", cascade = "all, delete", lazy = True)

class Questions(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key = True)
    question = db.Column(db.String, nullable = False)
    option_a = db.Column(db.String, nullable = False)
    option_b = db.Column(db.String, nullable = False)
    option_c = db.Column(db.String, nullable = False)
    option_d = db.Column(db.String, nullable = False)
    correct_option = db.Column(db.String, nullable = False)
    mark = db.Column(db.Integer, nullable = False)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id"), nullable = False)

class Scores(db.Model):
    __tablename__ = 'scores'
    id = db.Column(db.Integer, primary_key = True)
    total_score = db.Column(db.Integer, nullable = False)
    submitted_at = db.Column(db.DateTime, nullable=False, default=func.now())
    total_attempted_questions = db.Column(db.Integer, nullable = False)
    total_correct_answers = db.Column(db.Integer, nullable = False)
    total_wrong_answers = db.Column(db.Integer, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id"), nullable = False)


