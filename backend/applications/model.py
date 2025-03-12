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
    role = db.Column(db.String, nullable = False, default = 'user') #['admin', 'user']
    email = db.Column(db.String, unique = True, nullable = False)
    password = db.Column(db.String(20), nullable = False)
    name = db.Column(db.String(20), nullable = False)
    qualification = db.Column(db.String(20), default = 'Beginner') #['Beginner', 'Intermediate', 'Advanced']
    dob = db.Column(db.Date)
    reminder_time = db.Column(db.Time, default = time(17, 0, 0)) #default time for sending reminders is 5 pm
    user_activity = db.relationship("UserActivity", backref = "user", cascade = "all, delete", lazy = True)
    subjects = db.relationship("Subject", secondary = user_subject, backref = "users", lazy = True)
    scores = db.relationship("Scores", backref = "user", cascade = "all, delete", lazy = True)
    student_answers = db.relationship("StudentAnswer", backref = "user", cascade = "all, delete", lazy = True)
#add option to upload image in all users, subjects, chapters

class UserActivity(db.Model):
    __tablename__ = 'user_activity'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    last_visited = db.Column(db.Date, nullable=False)


class Subject(db.Model):
    __tablename__ = 'subject'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False, unique = True)
    description = db.Column(db.String)
    chapters = db.relationship("Chapter", backref = "subject", cascade = "all, delete", lazy = True)

    def convert_to_json(self):
        return{
            "id" : self.id,
            "name" : self.name,
            "description" : self.description,
            "chapters" : [chapter.name for chapter in self.chapters]
        }
    

class Chapter(db.Model):
    __tablename__ = 'chapter'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    description = db.Column(db.String)
    subject_id = db.Column(db.Integer, db.ForeignKey("subject.id"), nullable = False)
    quizzes = db.relationship("Quiz", backref = "chapter", cascade = "all, delete", lazy = True)
    
    def convert_to_json(self):
        return{
            "id" : self.id,
            "name" : self.name,
            "description" : self.description,
            "subject_id" : self.subject_id,
            "subject_name" : self.subject.name,
            "quizzes" : [quiz.name for quiz in self.quizzes]
        }

class Quiz(db.Model):
    __tablename__ = 'quiz'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    level = db.Column(db.String, nullable = False) #['Beginner', 'Intermediate', 'Advanced']
    date_of_quiz = db.Column(db.Date, nullable = False)
    time_of_quiz = db.Column(db.Time,  default = time(10, 0, 0))
    time_duration = db.Column(db.Time, default = time(1,00)) # format - hh:mm - 01:00
    remarks = db.Column(db.String)
    chapter_id = db.Column(db.Integer, db.ForeignKey("chapter.id"), nullable = False)
    questions = db.relationship("Questions", backref = "quiz", cascade = "all, delete", lazy = True)
    scores = db.relationship("Scores", backref = "quiz", cascade = "all, delete", lazy = True)
#Add number of question 

    def convert_to_json(self):
        return{
            "id" : self.id,
            "name" : self.name,
            "level" : self.level,
            "date_of_quiz" : self.date_of_quiz.strftime('%d-%m-%Y') if self.date_of_quiz else None,  
            "time_of_quiz" : self.time_of_quiz.strftime("%H:%M:%S") if self.time_of_quiz else None,
            "time_duration" : self.time_duration.strftime("%H:%M") if self.time_duration else None,
            "remarks" : self.remarks,
            "chapter_id" : self.chapter_id,
            "chapter_name" : self.chapter.name,
            "num_questions" : len(self.questions),
            "subject_name" : self.chapter.subject.name
        }

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
    student_answers = db.relationship("StudentAnswer", backref = "question", cascade = "all, delete", lazy = True)

    def convert_to_json(self):
        return{
            "id" : self.id,
            "question" : self.question,
            "option_a" : self.option_a,
            "option_b" : self.option_b,  
            "option_c" : self.option_c,
            "option_d" : self.option_d,
            "correct_option" : self.correct_option,
            "mark" : self.mark,
            "quiz_id" : self.quiz_id,
            "quiz_name" : self.quiz.name
        }

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
    student_answers = db.relationship("StudentAnswer", backref = "score", cascade = "all, delete", lazy = True)

    def convert_to_json(self):
        return{
            "id" : self.id,
            "total_score" : self.total_score,
            "submitted_at" : self.submitted_at.strftime('%d-%m-%Y %H:%M:%S'),
            "total_attempted_questions" : self.total_attempted_questions,
            "total_correct_answers" : self.total_correct_answers,
            "total_wrong_answers" : self.total_wrong_answers,
            "user_id" : self.user_id,
            "user_name" : self.user.name,
            "quiz_id" : self.quiz_id,
            "quiz_name" : self.quiz.name,
            "chapter_name" : self.quiz.chapter.name,
            "subject_name" : self.quiz.chapter.subject.name,
            "num_questions" : len(self.quiz.questions),
            "total_quiz_score" : sum(question.mark for question in self.quiz.questions)
        }

class StudentAnswer(db.Model):
    __tablename__ = "student_answer"
    id = db.Column(db.Integer, primary_key = True)
    selected_option = db.Column(db.String(20))
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"),nullable=False)
    score_id = db.Column(db.Integer, db.ForeignKey("scores.id"),nullable=False)

