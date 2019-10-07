from securepi import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"User('{self.id}', '{self.email}', '{self.password}')"

class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    notifications = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"Email('{self.id}', '{self.email}', '{self.notifications}')"

class Records(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = (db.DateTime(timezone=False))
    file_type = (db.Column(db.String(100), nullable=False))
    path_filename = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"Picture('{self.id}', '{self.created_at}', '{self.file_type}', '{self.path_filename}')"
