import datetime

from flask import Flask, request
from flask_restplus import Resource, Api, fields
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

api = Api(app)

# Database Models

class User(db.Model):
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    write_fields = {'username': fields.String,
                    'email': fields.String,
                    }
    read_fields = {'userid': fields.Integer,
                   'username': fields.String,
                   'email': fields.String,
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

def update_obj_with(obj, json, keys):
    for key in keys:
        if key in json:
            setattr(obj, key, json[key])


# Endpoints

PostUserRequest = api.model('PostUserRequest', User.write_fields)
PostUserResponse = api.model('PostUserResponse', User.read_fields)
GetUserResponse = api.model('GetUserResponse', User.read_fields)
PutUserRequest = api.model('PutUserRequest', User.write_fields)
PutUserResponse = api.model('PutUserResponse', User.read_fields)

@api.route('/api/user')
class CreateUserEndpoint(Resource):

    @api.expect(PostUserRequest)
    @api.doc(model=PostUserResponse)
    @api.marshal_with(PostUserResponse)
    def post(self):
        # TODO do something more graceful when integrity constraints are violated.
        json = request.json
        user = User()
        update_obj_with(user, json, User.write_fields.iterkeys())
        db.session.add(user)
        db.session.commit()
        return user


@api.route('/api/user/<int:userid>')
class UserEndpoint(Resource):

    @api.doc(model=GetUserResponse)
    @api.marshal_with(GetUserResponse)
    def get(self, userid):
        user = User.query.filter_by(userid=userid).first_or_404()
        return user

    @api.expect(PutUserRequest)
    @api.doc(model=PutUserResponse)
    @api.marshal_with(PutUserResponse)
    def put(self, userid):
        # TODO do something more graceful when integrity constraints are violated.
        user = User.query.filter_by(userid=userid).first_or_404()
        update_obj_with(user, request.json, User.write_fields.iterkeys())
        db.session.add(user)
        db.session.commit()
        return user

GetGoalResponse = api.model('GetGoalResponse', Goal.read_fields)
PutGoalRequest = api.model('PutGoalRequest', Goal.write_fields)
PutGoalResponse = api.model('PutGoalResponse', Goal.read_fields)
GoalPostRequest = api.model('GoalPostRequest', Goal.write_fields)
GoalPostResponse = api.model('GoalPostResponse', Goal.read_fields)
UserGoalsResponse = api.model('UserGoalsResponse', {
    'goals': fields.List(fields.Nested(GetGoalResponse))
})

@api.route('/api/goal/<int:goalid>')
class GoalEndpoint(Resource):

    @api.doc(model=GetGoalResponse)
    @api.marshal_with(GetGoalResponse)
    def get(self, goalid):
        goal = Goal.query.filter_by(goalid=goalid).first_or_404()
        return goal

    @api.expect(PutGoalRequest)
    @api.doc(model=PutGoalResponse)
    @api.marshal_with(PutGoalResponse)
    def put(self, goalid):
        # TODO do something more graceful when integrity constraints are violated.
        goal = Goal.query.filter_by(goalid=goalid).first_or_404()
        for field in Goal.write_fields:
            setattr(goal, field, request.json[field])
        db.session.add(goal)
        db.session.commit()
        return goal


@api.route('/api/goal/<int:goalid>/markdone')
class MarkDoneEndpoint(Resource):

    def post(self, goalid):
    	db.session.query(Goal).filter(Goal.goalid == goalid).update(
            {'lastDone': datetime.datetime.now()})
        db.session.commit()


@api.route('/api/user/<int:userid>/goals')
class UserGoals(Resource):

    @api.doc(model=UserGoalsResponse)
    @api.marshal_with(UserGoalsResponse)
    def get(self, userid):
        user = User.query.filter_by(userid=userid).first_or_404()
        goals = user.goals.all()
        return {'goals': goals}


@api.route('/api/user/<int:userid>/goal')
class UserGoal(Resource):

    @api.expect(GoalPostRequest)
    @api.doc(model=GoalPostResponse)
    @api.marshal_with(GoalPostResponse)
    def post(self, userid):
        user = User.query.filter_by(userid=userid).first_or_404()
        goal = Goal(user=user)
        update_obj_with(goal, request.json, Goal.write_fields.iterkeys())
        db.session.add(goal)
        db.session.commit()
        return goal


if __name__ == '__main__':
    app.run(debug=True)
