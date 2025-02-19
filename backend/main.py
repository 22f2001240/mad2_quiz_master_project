from flask import Flask
from applications.model import *

app = Flask(__name__)
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

if __name__ == "__main__":
    db.create_all()
    add_admin()
    app.run(debug = True)
