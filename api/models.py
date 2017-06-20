from flask_restplus import fields
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)

    write_fields = {'username': fields.String,
                    }
    read_fields = {'userid': fields.Integer,
                   'username': fields.String,
                   }

    def __repr__(self):
        return '<User %r>' % self.userid


class Goal(db.Model):
    goalid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    lastDone = db.Column(db.DateTime)
    userid = db.Column(db.Integer, db.ForeignKey('user.userid'))
    user = db.relationship('User', backref=db.backref('goals', lazy='dynamic'))

    write_fields = {'name': fields.String}
    read_fields = {'name': fields.String,
                   'goalid': fields.Integer,
                   'lastDone': fields.DateTime,
                   'userid': fields.Integer,
                   }

    def __init__(self, user):
        self.user = user

    def __repr__(self):
        return '<Goal %r>' % self.goalid
