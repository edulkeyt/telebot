function wheelsStateController(wheelsStateContainer, updateAction, updateTimeInterval){
	function changeStateValue(leftWheelState, rightWheelState){
		
	}
	
	return {
		stateContainer: wheelsStateContainer,
		updateState: function(newStateCommand){
			
		}
	};
}

function wheelsSatetController(_leftWheelState, _rightWheelState){
	this.setState = function(leftWheelState, rightwheelstate){ _leftWheelState=leftWheelState; _rightWheelState=rightWheelState; };
	this.getState = function(){}
}

 