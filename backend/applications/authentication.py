from flask import current_app as app,request
from flask_restful import Resource
from .model import *
from datetime import datetime

class LoginAPI(Resource):
    def post(self):
        data = request.json
        required_fields = ['email', 'password']
        if not all(field in data and data[field] for field in required_fields):
            return {"message" : 'Bad request! All fields are required.'}, 400
        email = data.get("email")
        password = data.get("password")
        user = User.query.filter_by(email = email).first()
        if user:
            if not user.password == password:
                return {"message" : "Incorrect Password"},401
            return {"message" : "Login Successful !"},200
        return {"message" : "User not found. Please check your username and password "}
    
class SignupAPI(Resource):
    def post(self):
        data = request.json
        required_fields = ['email', 'password', 'name']
        if not all(field in data and data[field] for field in required_fields):
            return {"message" : 'Bad request! All fields are required.'}, 400
        email, password, name, qualification = data.get("email"), data.get("password"), data.get("name"), data.get("qualification")
        dob_str = data.get("dob")
        dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
        reminder_time_str = data.get("reminder_time", "17:00:00")  
        reminder_time = datetime.strptime(reminder_time_str, "%H:%M:%S").time()
        subject_names = data.get("subjects",[])  # List of subject names
        user = User.query.filter_by(email = email).first()
        if user:
            return {"message": "User already exists! Please login"}, 409
        subjects = []
        if subject_names:
            subjects = Subject.query.filter(Subject.name.in_(subject_names)).all()
            if not subjects:
                return {"message": "Invalid subjects provided!"}, 400
        new_user = User(email = email, password = password, name = name, qualification = qualification, dob = dob, subjects=subjects, reminder_time = reminder_time)
        db.session.add(new_user)
        db.session.commit()
        return {"message" : "User registered successfully", "user_id": new_user.id},201
        