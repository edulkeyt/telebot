function joystickBase(minAngle, maxAngle, initParams){//controlArea, servoX, servoY, onMoveAction){
				
	var touchX, touchY;
	
	function findTouchByTarget(touchList, targetElem){
					
		for(var i=0; i < touchList.length; i++){
			if(touchList[i].target == targetElem) return touchList[i];
		}
					
		return null;
	}
				
	function start(e) {
		var touch = findTouchByTarget(e.touches, initParams.controlArea);
		touchX = touch.pageX;
		touchY = touch.pageY;
	}
				
	function move(e) {
		
		function applyServoAngles(movX, movY){

			function posToAngle(servo, pos){
				servo.angle += ~~(pos*servo.speed);
				if(servo.angle <= minAngle(servo)) return servo.angle = servo.minAngle;
				if(servo.angle >= maxAngle(servo)) return servo.angle = servo.maxAngle;
				return servo.angle;
			}
		
			posToAngle(initParams.servoX, movX);
			posToAngle(initParams.servoY, movY);
		}
		
		e.preventDefault();
		var touch = findTouchByTarget(e.touches, initParams.controlArea);
		movX = touch.pageX - touchX;
		movY = touch.pageY - touchY;
		applyServoAngles(touch.pageX - touchX, touch.pageY - touchY);
		initParams.onMoveAction();
		touchX = touch.pageX;
		touchY = touch.pageY;
	}
				
	initParams.controlArea.addEventListener("touchstart", start, true);
	initParams.controlArea.addEventListener("touchmove", move, true);
	
	return { control:initParams.controlArea, start:start, move:move };
}

function joystick(controlArea, servoX, servoY, onMoveAction){
	return joystickBase(
		function(servo){return servo.minAngle;},
		function(servo){return servo.maxAngle;}, 
		{controlArea:controlArea, servoX:servoX, servoY:servoY, onMoveAction:onMoveAction});
}

function calibrationJoystick(controlArea, servoX, servoY, onMoveAction){
	return joystickBase(
		function(servo){return 0;},
		function(servo){return 180;}, 
		{controlArea:controlArea, servoX:servoX, servoY:servoY, onMoveAction:onMoveAction});
}

function removeBinding(servoBinding){
	if(servoBinding == null) return;	
	servoBinding.control.removeEventListener("touchstart", servoBinding.start, true);
	servoBinding.control.removeEventListener("touchmove", servoBinding.move, true);
}