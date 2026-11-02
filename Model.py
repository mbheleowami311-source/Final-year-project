from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable= False)
    surname = db.Column(db.String(100), nullable= True)
    email = db.Column(db.String(100), nullable= False, unique=True)
    password = db.Column(db.String(100), nullable= False)
    phone_no = db.Column(db.String(100), nullable= False)
    status = db.Column(db.String(100), nullable= True)
    role = db.Column(db.String(100), default = "user")
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable= False)
    surname = db.Column(db.String(100), nullable= False)
    email = db.Column(db.String(100), nullable= False, unique=True)
    password = db.Column(db.String(100), nullable= False)
    phone_no = db.Column(db.String(100), nullable= False)
    status = db.Column(db.String(100), nullable= True)
    role = db.Column(db.String(100), default = "admin")
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # def is_Empty(self):
    #     return self.query.count()==0


class RankM(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable= False)
    surname = db.Column(db.String(100), nullable= False)
    email = db.Column(db.String(100), nullable= False, unique=True)
    password = db.Column(db.String(100), nullable= False)
    phone_no = db.Column(db.String(100), nullable= False)
    status = db.Column(db.String(100), nullable= True)
    role = db.Column(db.String(100), default = "RankManager")
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


class TaxiDriver(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable= False)
    surname = db.Column(db.String(100), nullable= False)
    email = db.Column(db.String(100), nullable= False, unique=True)
    password = db.Column(db.String(100), nullable= False)
    phone_no = db.Column(db.String(100), nullable= False)
    status = db.Column(db.String(100), nullable= True)
    taxi_no = db.Column(db.String(100), nullable= True)
    role = db.Column(db.String(100), default = "TaxiDriver")
    date_created = db.Column(db.DateTime, default=datetime.utcnow)



class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable= False)
    complaint_type = db.Column(db.String(100), nullable= False)
    location = db.Column(db.String(100), nullable= False)
    details = db.Column(db.String(100), nullable= False, unique=True)
    status = db.Column(db.String(100), nullable= True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

# class Location(db.Model):
#     id = db.Column(db.Integer, primary_key = True),
#     name = db.Column(db.String(100), nullable= True),
#     location = db.Column(db.String(100), nullable= False),
#     details = db.Column(db.String(100), nullable= False, unique=True)
#     status = db.Column(db.String(100), nullable= True)
#     date_created = db.Column(db.DateTime, default=datetime.utcnow)


class Indawo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    fk_id = db.Column(db.Integer, nullable = True)
    location = db.Column(db.String(100), nullable= False)
    how_many = db.Column(db.String(100), nullable= False, unique=True)
    status= db.Column(db.String(100), nullable= True, default= "pending")
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    assigned_driver= db.Column(db.String(100), nullable= True)






