const wheelForward = 1;
const wheelStop = 0;
const wheelBack = 2;

function wheelsJoystick(joystickDiv, _strictAreaRadius, setWheelsState){
    
    //start move to function parameters

    //let _strictAreaRadius = 20;

    /*function setWheelsState(leftWheelDirection, rightWheelDirection){//, leftWheelSpeed, RightWheelSpeed){
        let directionLetters = ['b', 's', 'f'];        
        console.clear();
        console.log(directionLetters[leftWheelDirection + 1] + directionLetters[rightWheelDirection + 1]);
    }*/

    //end

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
            
            setWheelsState(calculateWheelDirection(leftWheelAxisCoord), calculateWheelDirection(rightWheelAxisCoord));
        }

        e.preventDefault();
        let touch = findTouchByTarget(e.touches, joystickDiv);
        let joystickX = touch.pageX - joysticCenterX;
        let joystickY = touch.pageY - joysticCenterY;
        calculateWheelsState(-joystickX, -joystickY, _strictAreaRadius, _joystickWidth);
    }

    joystickDiv.addEventListener("touchmove", move, true);
}