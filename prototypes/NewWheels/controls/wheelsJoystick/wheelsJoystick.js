const wheelForward = 1;
const wheelStop = 0;
const wheelBack = -1;

function wheelsJoystick(joystickDiv){
    
    //start move to function parameters
    let _strictArea = {
        left: 30,
        right: 30,
        top: 30,
        bottom: 30,
        borderLeft: 60,
        borderRight: 60
    }

    let wheelSpeed = {
        max: 180,
        min: 0
    }

    function setWheelsState(leftWheelDirection, rightWheelDirection){//, leftWheelSpeed, RightWheelSpeed){
        let directionLetters = ['b', 's', 'f'];        
        console.clear();
        console.log(directionLetters[leftWheelDirection + 1] + directionLetters[rightWheelDirection + 1]);
    }

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

        function calculateWheelsState(x, y, strictArea,  joystickWidth){

            let joystickHalfWidth = joystickWidth / 2;

            /*function getSpeed(x, y, yOffset, ){

            }*/

            function movingCases(x, y, mainDirection, strictArea,  joystickHalfWidth){
                
                if(x < -strictArea.left){
                    //mainDirection and left cases
                    if(x < strictArea.borderLeft - joystickHalfWidth){
                        //rotate around left wheel
                        setWheelsState(wheelStop, mainDirection);
                        return;
                    }
                    //move and turn left 
                    setWheelsState(mainDirection, mainDirection);
                    return;
                }

                if(x > strictArea.right){
                    //mainDirection and right cases
                    if(x > joystickHalfWidth - strictArea.borderRight){
                        //rotate around right wheel
                        setWheelsState(mainDirection, wheelStop);
                        return;
                    }
                    //move and turn right case
                    setWheelsState(mainDirection, mainDirection)
                    return;
                }
                //strickly to main dirrection
                setWheelsState(mainDirection, mainDirection);                
            }

            function rotateOnPointCases(x, y, strictArea,  joystickHalfWidth){
                if(x < -strictArea.left){
                    //rotate left on a point
                    setWheelsState(wheelBack, wheelForward);
                    return;
                }
                if(x > strictArea.right){
                    //rotate right on a point
                    setWheelsState(wheelForward, wheelBack);
                    return;
                }
                //center of joystick 
                setWheelsState(wheelStop, wheelStop);
            }

            if(y < -strictArea.top){
                //forward cases
                movingCases(x, y, wheelForward,strictArea,  joystickHalfWidth);
                return;
            }

            if(y > strictArea.bottom){
                //back cases
                movingCases(x, y, wheelBack, strictArea,  joystickHalfWidth);
                return;
            }

            rotateOnPointCases(x, y, strictArea,  joystickHalfWidth);
        }

        e.preventDefault();
        let touch = findTouchByTarget(e.touches, joystickDiv);
        let joystickX = touch.pageX - joysticCenterX;
        let joystickY = touch.pageY - joysticCenterY;
        calculateWheelsState(joystickX, joystickY, _strictArea, _joystickWidth);
    }

    joystickDiv.addEventListener("touchmove", move, true);
}

$(document).ready(function(){

    var wheelsJoysticks = $(".wheels-joystick");

    wheelsJoysticks.each(function(index, item){

        var wheelsJoystickDiv = item;

        wheelsJoystick(wheelsJoystickDiv);
    })    
})


/*if(x > strictArea.left && x < strictArea.right){
                if(y >= strictArea.top && y <= strictArea.bottom){
                    return;
                }
                //forward or back
                return;
            }
            if(y > strictArea.top && y < strictArea.bottom){
                //rotate on one point
                return;
            }
            if(x < (-0.5) * joystickWidth + strictArea.borderLeft){
                //rotate around left wheel
                return;
            }
            if(x > joystickWidth / 2 - strictArea.borderRight){
                //rotate around right wheel
                return;
            }
            //mixed
            return
            */