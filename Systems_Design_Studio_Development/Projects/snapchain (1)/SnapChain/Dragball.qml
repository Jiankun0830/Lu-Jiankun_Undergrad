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

        MouseArea {
            anchors.fill: parent
            hoverEnabled: false
            onPositionChanged: { parent.color = 'red';
                // get the body under the mouse
                var tbody = ball.body;
                // get the current center of this body
                var currentLocation = tbody.getWorldCenter();
                // get the mouse coordinates (the target location)
                var x = mouse.x;
                var y = mouse.y;
                var absolutePos = mapToItem(null,x,y);
                x = absolutePos.x;
                y = absolutePos.y;
                //console.log("ball.x "+currentLocation.x+" mouse.x "+x);
                // get a vector pointing toward the target
                var direction = Qt.point(x-currentLocation.x,y-currentLocation.y);
                // compute the distance to the target
                var r = Math.sqrt(Math.pow(direction.x,2)+Math.pow(direction.y,2));

                // if the distance is big enough...
                if (r>1){
                    //normalize the direction
                    direction.x = direction.x/r;
                    direction.y = direction.y/r;

                    // set the desired speed to whatever you like: too fast makes behavior crazy
                    var desiredSpeed = 10;
                    // scale the normalized direction by the desired speed to get the desired velocity
//                            var desiredVelocity =Qt.point(desiredSpeed*direction.x,desiredSpeed*direction.y);
                    var desiredVelocity =Qt.point(desiredSpeed/Math.abs(direction.y)*direction.x,desiredSpeed/Math.abs(direction.y)*direction.y);
                    //console.log("x "+desiredVelocity.x+" y "+desiredVelocity.y);

                   //console.log("x "+tbody.linearVelocity.x+" y "+tbody.linearVelocity.y);

                    // set the linear velocity of this agent
                    tbody.linearVelocity.x= desiredVelocity.x;
                    tbody.linearVelocity.y= desiredVelocity.y;
                }}
        }
    }

}
