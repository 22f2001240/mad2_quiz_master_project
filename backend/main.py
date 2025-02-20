from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from datetime import timedelta
from applications.model import *
from applications.authentication_api import *
from applications.home import *
from applications.subject_api import *

app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///quizMasterDB"
app.config["JWT_SECRET_KEY"] = "quizMaster123"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours = 12)

db.init_app(app)
app.app_context().push()

def add_admin():
    admin = User.query.filter_by(role = "admin").first()
    if not admin:
        admin = User(email = "admin@gmail.com", password = "admin", name = "admin", role = "admin",qualification = '' )
        db.session.add(admin)
        db.session.commit()
        return "Admin added successfully"
    return "Admin is already in"




api.add_resource(HomeAPI,'/api/home')
api.add_resource(LoginAPI,'/api/login')
api.add_resource(SignupAPI,'/api/signup')
api.add_resource(SubjectAPI,'/api/subject','/api/subject/<int:subject_id>')




if __name__ == "__main__":
    db.create_all()
    add_admin()
    app.run(debug = True)
