from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from app import login
from app import db

class UserModel(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    about_me = db.Column(db.String(140))
    location = db.Column(db.String(20))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    
@login.user_loader
def load_user(id):
    return UserModel.query.get(int(id))

class RepositoryModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, index=True)
    description = db.Column(db.String(500))
    created_on = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id', name='issue_repository_fk'))
    user = db.relationship('UserModel', backref='repositories')
    issues = db.relationship('IssueModel', backref='repository', lazy='dynamic', foreign_keys='IssueModel.repository_id')
    
    def __repr__(self):
        return '<Repository {}>'.format(self.name)
    
    
class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), index=True) 

    def __repr__(self):
        return '<Status {}>'.format(self.title)
    
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), index=True)

    def __repr__(self):
        return '<Category {}>'.format(self.title)
    
class IssueModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), index=True)
    description = db.Column(db.String(400), index=True)

    status_id = db.Column(db.Integer, db.ForeignKey(
        'status.id', name='issue_status_fk'), nullable=False)
    status = db.relationship('Status', backref='issues')

    category_id = db.Column(db.Integer, db.ForeignKey(
        'category.id', name='issue_category_fk'), nullable=False)
    category = db.relationship('Category', backref='issues') 

    created_by_id = db.Column(db.Integer, db.ForeignKey(
        'user_model.id', name='issue_user_fk'), nullable=False)
    created_by = db.relationship(
        'UserModel', backref='created_issues', foreign_keys=[created_by_id])

    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    repository_id = db.Column(db.Integer, db.ForeignKey(
        'repository_model.id', name='issue_repository_fk'), nullable=False)

    def __repr__(self):
        return '<Issue {}>'.format(self.title)