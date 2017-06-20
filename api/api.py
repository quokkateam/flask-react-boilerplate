import datetime

from flask import Flask, request
from flask_restplus import Resource, Api, fields

from models import db, User, Goal

PROD_CONFIG = {
    'SQLALCHEMY_DATABASE_URI': 'sqlite:////tmp/test.db',
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
}

api = Api(validate=True)


def set_config(app, config_dict):
    for key, val in config_dict.iteritems():
        app.config[key] = val


def create_app(config):
    app = Flask(__name__)
    set_config(app, config)
    db.init_app(app)
    api.init_app(app)
    return app


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


def get_now():
    return datetime.datetime.now()


@api.route('/api/goal/<int:goalid>/markdone')
class MarkDoneEndpoint(Resource):

    def post(self, goalid):
    	db.session.query(Goal).filter(Goal.goalid == goalid).update(
            {'lastDone': get_now()})
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
    app = create_app(PROD_CONFIG)
    app.run(debug=True)
