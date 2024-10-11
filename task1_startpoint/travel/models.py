from . import db
from flask_login import UserMixin
from datetime import datetime

class Destination(db.Model):
    """def __init__(self, name, description, image, currency):
        self.name = name
        self.description = description
        self.image = image
        self.currency = currency
        self.comments = []
    
    def set_comments(self, comment):
        self.comments.append(comment)"""
    __tablename__ = 'destinations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(200))
    image = db.Column(db.String(400))
    currency = db.Column(db.String(3))
    # ... Create the Comments db.relationship
	# relation to call destination.comments and comment.destination
    comments = db.relationship('Comment', backref='destination')

    # to make sure it knows that destination_id is being used as the id for the Destination class
    #def get_id(self):
    #       return (self.destination_id)



class Comment(db.Model):
    """def __init__(self, user, text, created_at):
        self.user = user
        self.text = text
        self.created_at = created_at"""
    __tablename__ = 'comments'
    comment_id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.now())
    # add the foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    id = db.Column(db.Integer, db.ForeignKey('destinations.id'))

    # to make sure it knows that comment_id is being used as the id for the Comment class
    def get_id(self):
           return (self.comment_id)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    comments = db.relationship('Comment', backref='user')

    # to make sure it knows that user_id is being used as the id for the User class
    def get_id(self):
           return (self.user_id)
