function testWheelState(){
	
	function testStop(){
		return [wheelState().is(0).stop === true, wheelState().is(1).stop === false, wheelState().is(2).stop === false, wheelState().is(3).stop === false];
	}
	
	function testForward(){
		return [wheelState().is(0).forward === false, wheelState().is(1).forward === true, wheelState().is(2).forward === false, wheelState().is(3).forward === false];
	}
		
	function testBack(){
		return [wheelState().is(0).back === false, wheelState().is(1).back === false, wheelState().is(2).back === true, wheelState().is(3).back === false];
	}
	
	function testNotChanged(){
		return [wheelState().is(0).notChanged === false, wheelState().is(1).notChanged === false, wheelState().is(2).notChanged === false, wheelState().is(3).notChanged === true];
	}
	
	return [testStop(), testForward(), testBack(), testNotChanged()];
}

function wheelState(){
	const forwardConst = 1;
	const backConst = 2;
	const stopConst = 0;
	const notChangedConst = 3;
	
	return {
		forward: 1,
		stop: 0,
		back: 2,
		notChanged: 3,
		is: function(oneWheelState){
			return {
				forward: oneWheelState === forwardConst,
				back: oneWheelState === backConst,
				stop: oneWheelState === stopConst,
				notChanged: oneWheelState === notChangedConst
			};
		}
	};
}

function getRightWheelState(wheelsState){ return wheelsState%4; }
function getLeftWheelState(wheelsState){ return Math.floor(wheelsState/4); }

function wheels(btnRightFwd, btnRightBck, btnLeftFwd, btnLeftBck, wheelsFunction){
		
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