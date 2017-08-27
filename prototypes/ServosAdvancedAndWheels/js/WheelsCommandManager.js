function wheels(btnRightFwd, btnRightBck, btnLeftFwd, btnLeftBck, wheelsFunction){
	
	function wheelState(){
		return {
			forward: 1,
			stop: 0,
			back: 2,
			notChanged: 3
		};
	}
	
	function wheelCommandString(rightWheelState, leftWheelState){
		return (rightWheelState + leftWheelState * 4).toString();
	}
	
	function bindButtonToWheelCommand(cButton, onPressCommandString, onReleaseCommandString){	
		console.log(cButton.id + " is initializing");
		console.log("onPressCommandString " + onPressCommandString);
		console.log("onReleaseCommandString" + onReleaseCommandString);
		cButton.addEventListener("touchstart", function(){wheelsFunction(onPressCommandString);}, true);
		cButton.addEventListener("touchend", function(){wheelsFunction(onReleaseCommandString);}, true);
	}
	
	var rightWheelStopCommandString = wheelCommandString(wheelState().stop, wheelState().notChanged);
	var rightWheelForwardCommandString = wheelCommandString(wheelState().forward, wheelState().notChanged);
	var rightWheelBackCommandString = wheelCommandString(wheelState().back, wheelState().notChanged)
	bindButtonToWheelCommand(btnRightFwd, rightWheelForwardCommandString, rightWheelStopCommandString)
	bindButtonToWheelCommand(btnRightBck, rightWheelBackCommandString, rightWheelStopCommandString)
	
	var leftWheelStopCommandString = wheelCommandString(wheelState().notChanged, wheelState().stop);
	var leftWheelForwardCommandString = wheelCommandString(wheelState().notChanged, wheelState().forward);
	var leftWheelBackCommandString = wheelCommandString(wheelState().notChanged, wheelState().back);
	bindButtonToWheelCommand(btnLeftFwd, leftWheelForwardCommandString, leftWheelStopCommandString);
	bindButtonToWheelCommand(btnLeftBck, leftWheelBackCommandString, leftWheelStopCommandString);	
}