from flask import current_app as app,request
from flask_restful import Resource
from flask_jwt_extended import jwt_required,get_jwt_identity
from datetime import datetime
from .model import *
from .home import *

class UserAPI(Resource):
    @jwt_required()
    @cache.cached(timeout=10)
    def get(self):
        users = User.query.filter_by(role='user').all() 
        user_json = []
        for user in users:
            user_json.append(user.convert_to_json())
        return user_json,200
    
    @jwt_required()
    @cache.cached(timeout=10)
    def put(self):
        user_id = get_jwt_identity()
        data = request.json
        # return {"message":data.get("reminder_time")}
        user = User.query.filter_by(id=user_id).first() 
        dob_str = data.get("dob")
        dob = datetime.strptime(dob_str,"%Y-%m-%d").date()
        today = date.today()
        if dob > today:
            return {"message": "Invalid date of birth"}, 400
        user.dob = dob
        reminder_time_str = data.get("reminder_time")
        if reminder_time_str != user.reminder_time.isoformat():
            reminder_time_str = f"{reminder_time_str}:00"
            reminder_time = datetime.strptime(reminder_time_str,"%H:%M:%S").time()
            user.reminder_time = reminder_time
        user.name = data.get("name") if user.name != data.get("name") else user.name
        user.email = data.get('email') if user.email != data.get('email') else user.email
        if data.get("confirmPassword"):
            if data.get("password") != data.get("confirmPassword"):
                return {"message":"Password Not Matching"},404
            user.password = data.get("password")
        cache.clear()
        db.session.commit()
        return { "message" : "Profile updated successfuly"},200

class SingleUserAPI(Resource):
    @jwt_required()
    @cache.cached(timeout=10)
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.filter_by(id=user_id).first() 
        return user.convert_to_json(),200