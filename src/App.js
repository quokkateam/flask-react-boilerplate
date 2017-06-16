import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import Goals from './Goals.js';
import { List, Map } from 'immutable';

const MakeGoal = (name, key) => Map({
	"name": name,
	"key": key,
	// unclicked -> clickPendingConfirmation -> clickConfirmed
	//                          ^          |
	//                          |          -----> clickConfirmFailed
	//                          |                         |
	//                          ---------------------------
	"state": "unclicked"
});

class App extends Component {

	constructor(props) {
		super(props);
		this.state = {
			goals: List([MakeGoal("first", 1), MakeGoal("second", 2)])
		};
		this.handleGoalClick = this.handleGoalClick.bind(this);
		this.updateGoal = this.updateGoal.bind(this);
	}

	updateGoal(goal, state) {
		this.setState(({ goals }) => ({
			goals: goals.map(g => {
				if (g.get("key") === goal.get("key")) {
					return g.update("state", () => state)
				}
				return g;
			})
		}))
	}

	handleGoalClick(goal) {
		const state = goal.get("state");
		if (state === "unclicked" || state === "clickConfirmFailed") {
			this.updateGoal(goal, "clickPendingConfirmation")
			setTimeout(() => { this.updateGoal(goal, "clickConfirmed"); }, 1000);
		}
	}

	render() {
		return (
			<div className="App">
				<div className="App-header">
					<img src={logo} className="App-logo" alt="logo" />
					<h2>Welcome to React</h2>
				</div>
				<Goals goals={this.state.goals} handleGoalClick={this.handleGoalClick} />
			</div>
		);
	}
}

export default App;
