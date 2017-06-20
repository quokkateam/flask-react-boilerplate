import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import moxios from 'moxios'


describe('mocking axios requests', function () {

  describe('across entire suite', function () {

    beforeEach(function () {
      // import and pass your custom axios instance to this method
      moxios.install()
    })

    afterEach(function () {
      // import and pass your custom axios instance to this method
      moxios.uninstall()
    })

    it('renders without crashing', (done) => {
      const div = document.createElement('div');
      ReactDOM.render(<App />, div);

      moxios.wait(function () {
        let request = moxios.requests.mostRecent()
        request.respondWith({
          status: 200,
          response: {
            goals: [
              {
                lastDone: "2017-06-20T09:38:20.194657",
                userid: 1,
                goalid: 1,
                name: "some goal"
              }
            ]
          }
        }).then(() => done())
      })
    });

  })

})