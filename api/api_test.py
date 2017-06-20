import datetime
import json
import mock
import unittest

from flask import Flask
from flask_testing import TestCase

from api import create_app, db

GOAL1 = dict(name='goal 1',
             goalid=1,
             lastDone=None,
             userid=1,)

GOAL2 = dict(name='goal 2',
             goalid=2,
             lastDone=None,
             userid=1,)


class EndpointsTest(TestCase):

    def create_app(self):
        config = {
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
            'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        }
        return create_app(config)

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def requestHelper(self, path, method='GET', data=None):
        return self.client.open(
            method=method,
            path=path,
            headers=None if data is None else {
                'Content-Type': 'application/json'},
            data=None if data is None else json.dumps(data))

    def testPostGetPutGetUser(self):
        response = self.requestHelper(
            method='POST',
            path='/api/user',
            data=dict(username='myusername'))
        self.assertEquals(response.json, dict(
            userid=1,
            username='myusername',
        ))
        response = self.requestHelper(path='/api/user/1')
        self.assertEquals(response.json, dict(
            userid=1,
            username='myusername',
        ))
        response = self.requestHelper(
            method='PUT',
            path='/api/user/1',
            data=dict(username='newusername'))
        self.assertEquals(response.json, dict(
            userid=1,
            username='newusername',
        ))
        response = self.requestHelper(path='/api/user/1')
        self.assertEquals(response.json, dict(
            userid=1,
            username='newusername',
        ))

    @mock.patch('api.get_now', side_effect=lambda: datetime.datetime(2017, 6, 19, 17, 23, 17, 478968))
    def testPostGetPutGetMarkdoneGetGoal(self, get_now_function):
        response = self.requestHelper(
            method='POST',
            path='/api/user',
            data=dict(username='myusername'))
        self.assertEquals(response.json, dict(
            userid=1,
            username='myusername',
        ))
        response = self.requestHelper(
            method='POST',
            path='/api/user/1/goal',
            data=dict(name='brush your tooth'))
        self.assertEquals(response.json, dict(
            name='brush your tooth',
            goalid=1,
            lastDone=None,
            userid=1,))
        response = self.requestHelper(path='/api/goal/1')
        self.assertEquals(response.json, dict(
            name='brush your tooth',
            goalid=1,
            lastDone=None,
            userid=1,))
        response = self.requestHelper(
            method='PUT',
            path='/api/goal/1',
            data=dict(name='brush your teeth'))
        self.assertEquals(response.json, dict(
            name='brush your teeth',
            goalid=1,
            lastDone=None,
            userid=1,))
        response = self.requestHelper(path='/api/goal/1')
        self.assertEquals(response.json, dict(
            name='brush your teeth',
            goalid=1,
            lastDone=None,
            userid=1,))
        self.requestHelper(method='POST', path='/api/goal/1/markdone')
        response = self.requestHelper(path='/api/goal/1')
        self.assertEquals(response.json, dict(
            name='brush your teeth',
            goalid=1,
            lastDone=get_now_function().isoformat(),
            userid=1,))

    def testMultipleGoals(self):
        response = self.requestHelper(
            method='POST',
            path='/api/user',
            data=dict(username='myusername'))
        self.assertEquals(response.json, dict(
            userid=1,
            username='myusername',
        ))
        response = self.requestHelper(
            method='POST',
            path='/api/user/1/goal',
            data=dict(name='goal 1'))
        self.assertEquals(response.json, GOAL1)
        response = self.requestHelper(
            method='POST',
            path='/api/user/1/goal',
            data=dict(name='goal 2'))
        self.assertEquals(response.json, GOAL2)
        response = self.requestHelper(path='/api/user/1/goals')
        self.assertEquals(response.json, dict(goals=[GOAL1, GOAL2]))


if __name__ == '__main__':
    unittest.main()
