from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from datetime import datetime

db = SQLAlchemy()

class Episodes(db.Model, SerializerMixin):
    __tablename__ = 'episodes'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    number = db.Column(db.Integer, nullable=False)

    appearances = db.relationship(
        "Appearances", back_populates="episode", cascade="all, delete"
    )

    serialize_rules = ('-appearances.episode',)

    def to_dict(self):
     return {
        "id": self.id,
        "date": self.date.strftime("%-m/%-d/%y"),
        "number": self.number
    }

    def to_dict_with_appearances(self):
     return {
        "id": self.id,
        "date": self.date.strftime("%-m/%-d/%y"),
        "number": self.number,
        "appearances": [
            {
                "id": a.id,
                "episode_id": a.episode_id,
                "guest_id": a.guest_id,
                "rating": a.rating,
                "guest": {
                    "id": a.guest.id,
                    "name": a.guest.name,
                    "occupation": a.guest.occupation
                }
            } for a in self.appearances
        ]
    }



class Guests(db.Model, SerializerMixin):
    __tablename__ = 'guests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    occupation = db.Column(db.String(100), nullable=False)

    appearances = db.relationship(
        'Appearances', back_populates='guest', cascade="all, delete-orphan"
    )

    serialize_rules = ('-appearances.guest',)

    def to_dict(self):
     return {
        "id": self.id,
        "name": self.name,
        "occupation": self.occupation
    }


class Appearances(db.Model, SerializerMixin):
    __tablename__ = 'appearances'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)

    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id'), nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'), nullable=False)

    episode = db.relationship('Episodes', back_populates='appearances')
    guest = db.relationship('Guests', back_populates='appearances')

    serialize_rules = ('-episode.appearances', '-guest.appearances')

    def to_dict(self):
     return {
        "id": self.id,
        "rating": self.rating,
        "episode_id": self.episode_id,
        "guest_id": self.guest_id,
        "guest": self.guest.to_dict()
    }


    @validates('rating')
    def validate_rating(self, key, value):
        if not (1 <= value <= 5):
            raise ValueError("Rating must be between 1 and 5")
        return value
