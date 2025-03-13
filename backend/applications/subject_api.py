from flask import current_app as app,request
from flask_restful import Resource
from .model import *
from .home import *

class SubjectAPI(Resource):
    @jwt_required()
    @cache.cached(timeout=120)
    def get(self):
        subjects = Subject.query.all() 
        subject_json = []
        for subject in subjects:
            subject_json.append(subject.convert_to_json())
        return subject_json,200
    
    @jwt_required()
    @role_required('admin')
    def post(self):
        data = request.json
        required_field = ["name"]
        if not all(field in data and data[field] for field in required_field):
            return {"message" : 'Bad request! All fields are required.'}, 400
        name, description = data.get("name"), data.get("description")
        if len(name) <2 :
            return {"message" : "Name is too short. "},400
        subject = Subject.query.filter_by(name = name).first()
        if subject:
            return {"message" : "Subject already exist"},409
        new_subject = Subject(name = name, description = description)
        db.session.add(new_subject)
        db.session.commit()
        cache.clear()
        return {"message" : "Subject created successfully"},201
    
    @jwt_required()
    @role_required('admin')
    def put(self,subject_id):
        subject = Subject.query.get(subject_id)
        if not subject:
            return {"message" : "Subject not found"},404
        data = request.json
        subject.name = data.get("name") if data.get("name") else subject.name
        subject.description = data.get("description") if data.get("description") else subject.description
        db.session.commit()
        cache.clear()
        return {"message" : "Subject updated successfully"}, 200
    
    @jwt_required()
    @role_required('admin')
    def delete(self,subject_id):
        subject = Subject.query.get(subject_id)
        if not subject:
            return {"message" : "Subject not found"},404
        db.session.delete(subject)
        db.session.commit()
        cache.clear()
        return {"message" : "Subject deleted successfully"}, 200
    
class OneSubject(Resource):
    @jwt_required()
    @cache.cached(timeout=120)
    def get(self,subject_id):
        subject = Subject.query.get(subject_id)
        if not subject:
            return {"message" : "Subject not found"},404
        return subject.convert_to_json(),200
        
class ChapterSubject(Resource):
    @jwt_required()
    @cache.cached(timeout=120)
    def get(self,subject_id):
        chapters = Chapter.query.filter_by(subject_id = subject_id).all()
        if chapters ==[]:
            return {'message': 'No chapters for thus subject!'}, 404
        chapter_json = []
        for chapter in chapters:
            chapter_json.append(chapter.convert_to_json())
        return chapter_json,200