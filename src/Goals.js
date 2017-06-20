import React from 'react';
import './Goals.css'

const Goal = ({ goal, handleGoalClick }) => {
	const now = new Date();
	const lastDone = new Date(goal.get("lastDone"));
	const doneToday = now.getDate() === lastDone.getDate()
		&& now.getMonth() === lastDone.getMonth() && now.getFullYear() === lastDone.getFullYear();
	return (
		<div>
			<button type="button" className="Goal-Button" onClick={() => (handleGoalClick(goal))}>{goal.get("name")}</button>
			{"  "} 
			{`state: ${goal.get("state")}`}
			{"  "} 
			{`doneToday: ${doneToday}`}
			{"  "} 
			{`lastDone: ${goal.get("lastDone")}`}
		</div>
		
	);
};

const Goals = ({ goals, handleGoalClick }) => {
	return (
		<div className="Goals">
			<h2>Goals</h2>
			{goals.map(goal => <Goal goal={goal} key={goal.get("goalid")} handleGoalClick={handleGoalClick} />)}
		</div>
	);
}

export default Goals;
