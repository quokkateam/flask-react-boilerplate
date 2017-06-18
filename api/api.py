import datetime

from flask import Flask
from flask_restplus import Resource, Api, fields

app = Flask(__name__)
api = Api(app)

goal_model = api.model(
    'Goal', {
        'name': fields.String,
        'goalid': fields.Integer,
        'lastDone': fields.DateTime,
    }
)

goals_model = api.model(
    'Goals', {
        'goals': fields.List(fields.Nested(goal_model))
    }
)

goals = {
    1: {'name': 'First daily goal',
        'goalid': 1,
        'lastDone': '2017-06-17T17:26:07.528Z', },
    2: {'name': 'Second daily goal',
        'goalid': 2,
        'lastDone': '2017-06-17T17:26:07.528Z', },
}

@api.route('/goals/user/<int:userid>')
class UserById(Resource):

    @api.doc(model=goals_model)
    @api.doc(responses={
        200: 'Success',
        404: 'User not found',
    })
    def get(self, userid):
        return {'goals': goals.values()}

@api.route('/goal/<int:goalid>')
class GoalById(Resource):

    @api.doc(model=goal_model)
    @api.doc(responses={
        200: 'Success',
        404: 'Goal not found',
    })
    def get(self, goalid):
        try:
            return goals[goalid]
        except KeyError:
            return {'message': 'Not Found'}, 404

    @api.doc(model=goal_model)
    def post(self, goalid):
        """
        Mark this goal as completed at the current time.
        """
        try:
            goals[goalid]['lastDone'] = datetime.datetime.now().isoformat()
            return goals[goalid]
        except KeyError:
            return {'message': 'Not Found'}, 404

if __name__ == '__main__':
    app.run(debug=True)
