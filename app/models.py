from datetime import datetime
from time import time
import jwt
from app import db, login, app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32), index=True)
    last_name = db.Column(db.String(32), index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), index=True)
    phone = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    about_me = db.Column(db.String(500))
    last_viewed = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean)

    def __repr__(self):
        return '<User {}>'.format(self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64))
    student_email = db.Column(db.String(64), index=True)
    parent_name = db.Column(db.String(64))
    parent_email = db.Column(db.String(64))
    secondary_email = db.Column(db.String(64))
    timezone = db.Column(db.Integer)
    location = db.Column(db.String(128))
    status = db.Column(db.String(24), default = "active", index=True)
    pronouns = db.Column(db.String(32))
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutor.id'))

    def __repr__(self):
        return '<Student {}>'.format(self.student_name + " " + self.last_name)


class Tutor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(64), index=True)
    timezone = db.Column(db.Integer)
    status = db.Column(db.String(24), default = "active", index=True)
    students = db.relationship('Student', backref='tutor', lazy='dynamic')

    def __repr__(self):
        return '<Tutor {}>'.format(self.first_name + " " + self.last_name)


class TestDate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    test = db.Column(db.String(24))
    status = db.Column(db.String(24), default = "confirmed")
    reg_date = db.Column(db.Date)
    late_date = db.Column(db.Date)
    other_date = db.Column(db.Date)

    def __repr__(self):
        return '<TestDate {}>'.format(self.date)


student_test_dates = db.Table('student_test_dates',
    db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
    db.Column('test_date_id', db.Integer, db.ForeignKey('test_date.id'))
)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
