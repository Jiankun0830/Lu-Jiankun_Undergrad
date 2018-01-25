import QtQuick 2.0
import Box2D 2.0
import "shared"

PhysicsItem {
    id: ball

    width: 40
    height: 40

    bodyType: Body.Dynamic
    world: physicsWorld

    gravityScale: 0

    property color color: "#EFEFEF"

    fixtures:
        Circle {
        id:circle
        radius: ball.width / 2
        density: 1
        restitution: 0
    }

    Rectangle {
        radius: parent.width / 2
        border.color: "blue"
        color: "red"
        width: parent.width
        height: parent.height
        smooth: true
    }

    MultiPointTouchArea{
        anchors.fill: parent
        touchPoints: [
            TouchPoint {
                id: point1
            }

    ]
        onTouchUpdated: function(){
            // get the body under the mouse
            var tbody = ball.body;
            // get the current center of this body
            var currentLocation = tbody.getWorldCenter();
            // get a vector pointing toward the target
            var x=point1.x;
            var y=point1.y;
            var absolutePos = mapToItem(null,x,y);
            x =absolutePos.x;
            y = absolutePos.y;
            var direction = Qt.point(x-currentLocation.x,y-currentLocation.y);
            // compute the distance to the target
            var r = Math.sqrt(Math.pow(direction.x,2)+Math.pow(direction.y,2));
            if (r>1){
                direction.x = direction.x/r;
                direction.y = direction.y/r;

                // set the desired speed to whatever you like: too fast makes behavior crazy
                var desiredSpeed = 5;
                // scale the normalized direction by the desired speed to get the desired velocity
    //                        var desiredVelocity =Qt.point(desiredSpeed*direction.x,desiredSpeed*direction.y);
                var desiredVelocity =Qt.point(desiredSpeed/Math.abs(direction.y)*direction.x,desiredSpeed/Math.abs(direction.y)*direction.y);
                //console.log("x "+desiredVelocity.x+" y "+desiredVelocity.y);
                //console.log("x "+tbody.linearVelocity.x+" y "+tbody.linearVelocity.y);
                // set the linear velocity of this agent
                tbody.linearVelocity.x= desiredVelocity.x;
                tbody.linearVelocity.y= desiredVelocity.y;
            //tbody.linearVelocity.x=0.02*direction.x
            //tbody.linearVelocity.y=0.02*direction.y
            }
        }
    }
}





