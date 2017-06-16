import React from 'react';
import './Goals.css'

const Goal = ({ goal, handleGoalClick }) => {
	const className = goal.get("clicked") ? "Goal-Button" : "";
	return (
		<div>
			<button type="button" className={className} onClick={() => (handleGoalClick(goal.get("key")))}>{goal.get("name")}</button>
		</div>
	);
};

const Goals = ({ goals, handleGoalClick }) => (
	<div className="Goals">
		<h2>Goals</h2>
		{goals.map(goal => <Goal goal={goal} key={goal.get("key")} handleGoalClick={handleGoalClick}/>)}
	</div>
);

export default Goals;
