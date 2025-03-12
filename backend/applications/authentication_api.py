from flask import current_app as app,request
from flask_restful import Resource
from datetime import datetime
from flask_jwt_extended import create_access_token
import re
from .model import *

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
            
            access_token = create_access_token(identity = user.id, additional_claims = {"role": user.role })

            user_activity = UserActivity.query.filter_by(email = user.email).first()
            if user_activity:
                user_activity.last_visited = datetime.now().date()
            else :
                new_user_activity = UserActivity(user_id = user.id,email = user.email,last_visited=datetime.now().date())
                db.session.add(new_user_activity)
            db.session.commit()
            return {"message" : "Login Successful !", "token" : access_token, "user_role" : user.role},200
        
        return {"message" : "User not found. Please check your username and password "}
    
class SignupAPI(Resource):
    def post(self):
        data = request.json
        required_fields = ['email', 'password', 'name']
        if not all(field in data and data[field] for field in required_fields):
            return {"message" : 'Bad request! All fields are required.'}, 400
        email, password, name, qualification = data.get("email"), data.get("password"), data.get("name"), data.get("qualification")
        #Backend validation 
        email_regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
        if not re.match(email_regex,email) :
            return {"message":"Invalid email format!"}, 400
        if len(password) <= 3 :
            return {"message" : "Password is too short. Should be atleast 4 characters and atmost 20 characters"}
        if len(password) > 20 :
            return {"message" : "Password is too long. Should be atleast 4 characters and atmost 20 characters"}
        dob_str = data.get("dob")
        dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
        today = date.today()
        min_date = today.replace(year=today.year - 120)
        if dob < min_date:
            return {"message": "Invalid DOB! Age cannot be more than 120 years."}, 400
        if dob > today:
            return {"message": "Invalid DOB! Date of birth cannot be in the future."}, 400
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
        