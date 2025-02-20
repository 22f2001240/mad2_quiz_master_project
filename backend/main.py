from flask import Flask
from flask_restful import Api
from applications.model import *
from applications.authentication import *
from applications.home import *

app = Flask(__name__)
api = Api(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///quizMasterDB"

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





if __name__ == "__main__":
    db.create_all()
    add_admin()
    app.run(debug = True)
