from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Epic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    stories = db.relationship('Story', backref='epic', lazy=True)

class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    epic_id = db.Column(db.Integer, db.ForeignKey('epic.id'), nullable=False)
    total_points = db.Column(db.Float, nullable=True)
    tasks = db.relationship('Task', backref='story', lazy=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer, db.ForeignKey('story.id'), nullable=False)
    assignee = db.Column(db.String(128), nullable=False)
    status = db.Column(db.String(64), nullable=False)