import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import Goals from './Goals.js';
import { List, Map } from 'immutable';
import axios from 'axios';

const MakeGoal = (name, goalid, lastDone) => Map({
	"name": name,
	"goalid": goalid,
	"lastDone": lastDone,
	//     /---------------------------------------------\
	//    v                                              |
	// waitingForClick -> clickPendingConfirmation -> clickConfirmed
	//                          ^          |
	//                          |          -----> clickConfirmFailed
	//                          |                         |
	//                          ---------------------------
	"state": "waitingForClick",
});

class App extends Component {

	constructor(props) {
		super(props);
		this.state = {
			goals: List([])
		};
		this.handleGoalClick = this.handleGoalClick.bind(this);
		this.updateGoal = this.updateGoal.bind(this);
		this.updateGoalsFromApi = this.updateGoalsFromApi.bind(this);
		this.updateGoalFromApi = this.updateGoalFromApi.bind(this);
	}

	updateGoalsFromApi(res) {
		this.setState(() => ({
			goals: List(res.data.goals.map(({ name, goalid, lastDone }) =>
				MakeGoal(name, goalid, lastDone)))
		}));
	}

	updateGoalFromApi(res) {
		const goalFromApi = res.data;
		this.setState(({ goals }) => ({
			goals: goals.map(g => {
				if (g.get("goalid") === goalFromApi.goalid) {
					return g
						.update("state", () => "clickConfirmed")
						.update("lastDone", () => goalFromApi.lastDone);
				}
				return g;
			})
		}));
	}

	componentDidMount() {
		axios.get('/goals/user/1')
			.then(this.updateGoalsFromApi);
	}

	updateGoal(goal, state) {
		this.setState(({ goals }) => ({
			goals: goals.map(g => {
				if (g.get("goalid") === goal.get("goalid")) {
					return g.update("state", () => state)
				}
				return g;
			})
		}))
	}

	handleGoalClick(goal) {
		const state = goal.get("state");
		if (state !== "clickPendingConfirmation") {
			this.updateGoal(goal, "clickPendingConfirmation")
			axios.post(`/goal/${goal.get("goalid")}`)
				.then((res) => {
					this.updateGoalFromApi(res);
					setTimeout(() => {
						this.updateGoal(goal, "waitingForClick");
					}, 1000);
				});
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
