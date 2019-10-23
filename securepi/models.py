#!/usr/bin/env python3

from securepi import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    notifications = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"User('{self.id}', '{self.email}', '{self.password}', '{self.notifications}')"

class Records(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = (db.Column(db.String(20), nullable=False))
    file_type = (db.Column(db.String(100), nullable=False))
    path_filename = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"Records('{self.id}', '{self.created_at}', '{self.file_type}', '{self.path_filename}')"

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'created_at': self.created_at,
            'file_type': self.file_type,
            'path_filename': self.path_filename,
        }
