import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import Goals from './Goals.js';
import { List, Map } from 'immutable';

const MakeGoal = (name, key) => Map({ "name": name, "key": key, "clicked": false });

class App extends Component {

	constructor(props) {
		super(props);
		this.state = {
			goals: List([MakeGoal("first", 1), MakeGoal("second", 2)])
		};
		this.handleGoalClick = this.handleGoalClick.bind(this)
	}

	handleGoalClick(key) {
		this.setState(({ goals }) => ({
			goals: goals.map(goal => {
				if (goal.get("key") === key) {
					return goal.update("clicked", (clicked) => !clicked);
				}
				return goal;
			})
		}))
	}

	render() {
		return (
			<div className="App">
				<div className="App-header">
					<img src={logo} className="App-logo" alt="logo" />
					<h2>Welcome to React</h2>
				</div>
				<p className="App-intro">
					To get started, edit <code>src/App.js</code> and save to reload.
				</p>
				<Goals goals={this.state.goals} handleGoalClick={this.handleGoalClick} />
			</div>
		);
	}
}

export default App;
