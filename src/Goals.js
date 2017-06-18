import React from 'react';
import './Goals.css'

const Goal = ({ goal, handleGoalClick }) => {
	return (
		<div>
			<button type="button" onClick={() => (handleGoalClick(goal))}>{goal.get("name")}</button>
			{"  "} 
			{goal.get("state")}
			{"  "} 
			{goal.get("lastDone")}
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
