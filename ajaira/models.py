from datetime import datetime
from ajaira import db,login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),nullable=True)
    email=db.Column(db.String(120),unique=True,nullable=False)
    image_file=db.Column(db.String(20),nullable=True,default="default.jpg")
    password=db.Column(db.String(60),nullable=True)
    posts=db.relationship("Post",backref='author',lazy=True)



    def __repr__(self):
        return "User('%s','%s','%s')"%(self.username,self.email,self.image_file)

class Post(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100),nullable=True)
    content=db.Column(db.Text,nullable=True)
    image=db.Column(db.String(20),nullable=True)
    date_posted=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    caption=db.Column(db.String(100),nullable=True)
    comment=db.Column(db.Text,nullable=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    def __repr__(self):
        return "Post('%s','%s')"%(self.title,self.date_posted)

class Voter(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(120),unique=True,nullable=False)
    def __init__(self, email):
        self.email = email

class Fighter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)


class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('votes', lazy='dynamic'))
    fighter_id = db.Column(db.Integer, db.ForeignKey('fighter.id'))
    fighter = db.relationship('Fighter', backref=db.backref('votes', lazy='dynamic'))
