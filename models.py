from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """user model"""
    __tablename__ = "users"
    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(30),nullable=False)
    last_name = db.Column(db.String(30),nullable=False)
    
    def ___repr___(self):
        return f'<User {self.username}>'
    

    @classmethod
    def registration(cls, username, password, email, first_name, last_name):
        """register username w/ hashsed password and return user"""

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")

        return User(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)

    @classmethod
    def authorization(cls, username, pwd):
        """Validate user exsits and authenticate with password"""

        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, pwd):
            return user
        else:
            return False
        
class Feedback(db.Model):
    """feedback model"""
    __tablename__="feedback"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable = False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(20), db.ForeignKey('users.username'))

    user = db.relationship('User',backref='feedback')

    def ___repr___(self):
        return f'<Feedback {self.id} {self.title} {self.username}>'