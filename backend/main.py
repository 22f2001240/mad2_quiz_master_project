from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from datetime import timedelta
from applications.worker import celery
from applications.task import *
from applications.model import *
from applications.authentication_api import *
from applications.home import *
from applications.subject_api import *
from applications.chapter_api import *
from applications.quiz_api import *
from applications.questions_api import *
from applications.scores_api import *


app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app)
cache=Cache()


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///quizMasterDB6"
app.config["JWT_SECRET_KEY"] = "quizMaster123"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours = 12)
#configure the caching for the flask
app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_HOST'] = 'localhost'
app.config['CACHE_REDIS_PORT'] = 6379
app.config['CACHE_REDIS_DB'] = 0
app.config['CACHE_REDIS_URL'] = "redis://localhost:6379"
app.config['CACHE_DEFAULT_TIMEOUT'] = 300

#setup celery
celery.conf.update(
    broker_url='redis://localhost:6379/0',
    result_backend='redis://localhost:6379/1',
    timezone = 'Asia/Kolkata'
)   


db.init_app(app)
cache.init_app(app)
app.app_context().push()


def add_admin():
    admin = User.query.filter_by(role = "admin").first()
    if not admin:
        admin = User(email = "admin@gmail.com", password = "admin", name = "admin", role = "admin",qualification = '' )
        db.session.add(admin)
        db.session.commit()
        return "Admin added successfully"
    return "Admin is already in"

@app.route('/test_cache')
@cache.cached(timeout=20)
def test_cache():
    time.sleep(10) #first it will sleep for 10 seconds then return testing is working . and this return will wait for 20 seconds. within this 20 sec. it will keep the return result so wont sleep for 10 seconds for calls inbetween this
    return "testing is working"

api.add_resource(HomeAPI,'/api/home')
api.add_resource(LoginAPI,'/api/login')
api.add_resource(SignupAPI,'/api/signup')
api.add_resource(SubjectAPI,'/api/subject','/api/subject/<int:subject_id>')
api.add_resource(OneSubject,'/api/subject/get/<int:subject_id>')
api.add_resource(ChapterSubject,'/api/subject/chapters/<int:subject_id>')
api.add_resource(ChapterAPI,'/api/chapter', '/api/chapter/crud/<int:chapter_id>')
api.add_resource(OneChapter,'/api/chapter/one/<int:chapter_id>')
api.add_resource(QuizAPI,'/api/quiz', '/api/quiz/<int:quiz_id>')
api.add_resource(ExportDataAPI,'/api/quiz/export')
api.add_resource(OneQuizAPI,'/api/quiz/one/<int:chapter_id>')
api.add_resource(SingleQuizAPI,'/api/single/quiz/<int:quiz_id>')
api.add_resource(CompletedQuizessStudentAPI,'/api/quiz/student/score')
api.add_resource(QuestionsAPI, '/api/question', '/api/question/<int:question_id>')
api.add_resource(QuizQuestionsAPI, '/api/quiz/question/<int:quiz_id>')
api.add_resource(SingleQuestionAPI,'/api/single/question/<int:question_id>')
api.add_resource(ScoresAPI,'/api/scores','/api/scores/<int:quiz_id>','/api/quiz/submit/<int:quiz_id>')




if __name__ == "__main__":
    db.create_all()
    add_admin()
    app.run(debug = True)
