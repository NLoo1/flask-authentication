from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()
bcrypt = Bcrypt()



class User(db.Model):

    __tablename__ = 'users_auth'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)

    @classmethod
    def register(cls, username, pwd, email,first_name,last_name):
        hashed = bcrypt.generate_password_hash(pwd)
        hashed_utf8 = hashed.decode("utf8")

        return cls(username=username, password=hashed_utf8, email=email,first_name=first_name,last_name=last_name)
    
    @classmethod
    def authenticate(cls, username, pwd):
        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            return u
        else:
            return False