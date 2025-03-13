from flask import current_app as app,request
from flask_restful import Resource
from .model import *
from .home import *

class ChapterAPI(Resource):
    @jwt_required()
    @cache.cached(timeout=120)
    def get(self):
        chapters = Chapter.query.all()
        if chapters ==[]:
            return {'message': 'No chapters found!'}, 404
        chapter_json = []
        for chapter in chapters:
            chapter_json.append(chapter.convert_to_json())
        return chapter_json,200

    @jwt_required()
    @role_required('admin')
    def post(self):
        data = request.json
        required_fields = ["name", "subject_id"]
        if not all(field in data and data[field] for field in required_fields):
            return {"message" : 'Bad request! All fields are required.'},400
        name, description, subject_id = data.get("name"), data.get("description"), data.get("subject_id")
        if len(name) <2 :
            return {"message" : "Name is too short. "},400
        subject = Subject.query.get(subject_id)
        if not subject:
            return {"message" : "Subject not found!"},404
        chapter = Chapter.query.filter_by(name = name, subject_id = subject_id).first()
        if chapter:
            return {"message" : "Chapter already exist!"},409
        new_chapter = Chapter(name = name, description = description, subject_id=subject_id)
        db.session.add(new_chapter)
        db.session.commit()
        cache.clear()
        return {"message" : "New Chapter added successfully"},201
    
    @jwt_required()
    @role_required('admin')
    def put(self,chapter_id):
        chapter = Chapter.query.get(chapter_id)
        if not chapter:
            return {"message" : "Chapter doest not found"}, 404
        data = request.json 
        chapter.name = data.get("name") if data.get("name") else chapter.name
        chapter.description = data.get("description") if data.get("description") else chapter.description
        chapter.subject_id = data.get("subject_id") if data.get("subject_id") else chapter.subject_id
        db.session.commit()
        cache.clear()
        return {"message" : "Chapter updated successfully"},200
    
    @jwt_required()
    @role_required('admin')
    def delete(self,chapter_id):
        chapter = Chapter.query.get(chapter_id)
        if not chapter:
            return {"message" : "Chapter not found"}, 404
        db.session.delete(chapter)
        db.session.commit()
        cache.clear()
        return {"message" : "Chapter deleted succesfully"}, 200

class OneChapter(Resource):
    @jwt_required()
    @cache.cached(timeout=120)
    def get(self,chapter_id):
        chapter = Chapter.query.get(chapter_id)
        if not chapter:
            return {"message" : "Chpater not found"},404
        return chapter.convert_to_json(),200