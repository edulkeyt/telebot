const wheelForward = 1;
const wheelStop = 0;
const wheelBack = 2;

function wheelsJoystick(joystickDiv, _strictAreaRadius, _maxSpeed, setWheelsState, stopAction){
    
    let _joystickWidth = $(joystickDiv).width();

    function getAbsoluteDivCenterX(div){
        return div.offset().left + div.width() / 2;
    }

    function getAbsoluteDivCenterY(div){
        return div.offset().top + div.height() / 2;
    }

    let joysticCenterX = getAbsoluteDivCenterX($(joystickDiv));
    let joysticCenterY = getAbsoluteDivCenterY($(joystickDiv));

    function move(e){

        function findTouchByTarget(touchList, targetElem){
            for(var i=0; i < touchList.length; i++){
                if(touchList[i].target == targetElem) return touchList[i];
            }
            return null;
        }

        function calculateWheelsState(leftWheelAxisCoord, rightWheelAxisCoord, strictAreaRadius, _joystickWidth){
            
            function calculateWheelDirection(wheelAxisCoord){
                if(wheelAxisCoord > strictAreaRadius) return wheelForward;
                if(wheelAxisCoord < -strictAreaRadius) return wheelBack;
                return wheelStop;
            }
            
            function calculateWheelSpeed(wheelAxisCoord, joystickRadius, maxSpeed){
                
                let speed;

                if(wheelAxisCoord > strictAreaRadius) speed = ~~((wheelAxisCoord - strictAreaRadius) * maxSpeed / (joystickRadius - 2 * strictAreaRadius));
                else if(wheelAxisCoord < -strictAreaRadius) speed = ~~(-(wheelAxisCoord + strictAreaRadius) * maxSpeed / (joystickRadius - 2 * strictAreaRadius));
                else speed = 0;
                
                if(speed >= maxSpeed) return maxSpeed;
                if(speed <= 0) return 0;
                return speed;
            }

            setWheelsState(
                calculateWheelDirection(leftWheelAxisCoord), 
                calculateWheelDirection(rightWheelAxisCoord),
                calculateWheelSpeed(leftWheelAxisCoord, _joystickWidth / 2, _maxSpeed),
                calculateWheelSpeed(rightWheelAxisCoord, _joystickWidth / 2, _maxSpeed)
            );
        }

        e.preventDefault();
        let touch = findTouchByTarget(e.touches, joystickDiv);
        let joystickX = touch.pageX - joysticCenterX;
        let joystickY = touch.pageY - joysticCenterY;
        calculateWheelsState(-joystickX, -joystickY, _strictAreaRadius, _joystickWidth);
    }

	function stop(e){
		e.preventDefault();
		stopAction();
	}
	
    joystickDiv.addEventListener("touchstart", move, true);
	joystickDiv.addEventListener("touchmove", move, true);
	if(typeof stopAction!= 'undefined' && stopAction !== null){
		joystickDiv.addEventListener("touchend", stop, true);
	}
}