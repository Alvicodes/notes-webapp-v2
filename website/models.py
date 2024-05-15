from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func #func gets the current date and time
import uuid

# Setting up classes to store data you want from the website. Below is one to many

class Note(db.Model):#all notes need to conform to the below parameters
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), server_default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #linking different information between users aka foreign keys. capitals for class in py but in sql doesn't matter hence user.id
    unique_number = db.Column(db.String(36), unique=True, nullable=False) #generate a unique number
    color = db.Column(db.String(20))
    def __init__(self, data, user_id):
        self.data = data
        self.user_id = user_id
        self.unique_number = str(uuid.uuid4())  # Generate unique number when creating a new Note

class User(db.Model, UserMixin): #all users need to conform to the below parameters
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note', backref='user') # relationship HERE NEEDS capital as it's referencing a CLASS DAW