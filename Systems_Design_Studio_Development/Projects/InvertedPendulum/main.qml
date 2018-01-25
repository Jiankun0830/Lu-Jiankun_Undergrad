import QtQuick 2.2
import Box2D 2.0
import QtQuick.Controls 1.1
import "shared"

ApplicationWindow {
    visible: true
    width: 2560
    height: 850
    title: "Inverted Pendulum"
Rectangle {
    id: screen
    width: parent.width
    height: parent.height
    color: "#EFEFFF"


    World { id: physicsWorld }

    Wall {
        id: topWall
        height: 20//40
        anchors {
            left: parent.left
            right: parent.right
            top: parent.top
        }
    }

    Wall {
        id: leftWall
        width: 20//40
        anchors {
            left: parent.left
            top: parent.top
            bottom: parent.bottom
            bottomMargin: 40
        }
    }

    Wall {
        id: rightWall
        width: 20//40
        anchors {
            right: parent.right
            top: parent.top
            bottom: parent.bottom
            bottomMargin: 40
        }
    }

    PhysicsItem {
        id: ground
        height: 40
        anchors {
            left: parent.left
            right: parent.right
            bottom: parent.bottom
        }
        fixtures: Box {
            width: ground.width
            height: ground.height
            friction: 1
            density: 1
        }
        Rectangle {
            anchors.fill: parent
            color: "#DEDEDE"
        }
    }


    PhysicsItem {  // this is the orange bar in between the two wheels
        id: body
        //property int speed: speedSlider.value
        //property int k: -1
        x: 650
        y: 780
        width: 100
        height: 20
        bodyType: Body.Dynamic
        fixtures: Box {
            width: body.width
            height: body.height
            density: 0.8
            friction: 0.5
            restitution: 0.8
        }
        Rectangle {
            anchors.fill: parent
            color: "orange"

            MouseArea {
                anchors.fill: parent
                hoverEnabled: false
                onPositionChanged: {
                    // get the body under the mouse
                    var tbody = body.body;
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
                        var desiredSpeed = 1;
                        // scale the normalized direction by the desired speed to get the desired velocity
//                            var desiredVelocity =Qt.point(desiredSpeed*direction.x,desiredSpeed*direction.y);
                        var desiredVelocity =Qt.point(desiredSpeed/Math.abs(direction.y)*direction.x,desiredSpeed/Math.abs(direction.y)*direction.y);
                        //console.log("x "+desiredVelocity.x+" y "+desiredVelocity.y);

                       //console.log("x "+tbody.linearVelocity.x+" y "+tbody.linearVelocity.y);

                        // set the linear velocity of this agent
                        tbody.linearVelocity.x= desiredVelocity.x;
                        tbody.linearVelocity.y= 0;
                    }}
            }





        }
    }
    PhysicsItem {
        id: wheelA
        x: 750
        y: 780
        width: 48
        height: 48
        bodyType: Body.Dynamic
        fixtures: Circle {
            radius: wheelA.width / 2
            density: 0.8
            friction: 10
            restitution: 0.8
        }
        Image {
            source: "images/wheel.png"
            anchors.fill: parent
        }
    }

    PhysicsItem {
        id: wheelB
        x: 650
        y: 780
        width: 48
        height: 48
        bodyType: Body.Dynamic
        fixtures: Circle {
            radius: wheelB.width / 2
            density: 0.8
            friction: 10
            restitution: 0.8
        }
        Image {
            source: "images/wheel.png"
            anchors.fill: parent
        }
    }

    PhysicsItem {
        id: rod
        sleepingAllowed: false
        bodyType: Body.Dynamic
        x: 695
        y: 380

        width: 20
        height: 120

        fixtures: Box {
            width: rod.width
            height: rod.height
            density: 0.1;
            friction: 1;
            restitution: 0.3;
        }

        Rectangle {
            color: "green"
            radius: 6
            anchors.fill: parent
        }
    }

    RevoluteJoint {
        id: revolute
        maxMotorTorque: 1000
        motorSpeed: 0
        enableMotor: false
        bodyA: body.body
        bodyB: rod.body
        localAnchorA: Qt.point(50,0)
        localAnchorB: Qt.point(10,120)
    }

    WheelJoint {
        id: wheelJointA
        bodyA: body.body
        bodyB: wheelA.body
        localAnchorA: Qt.point(100,10)
        localAnchorB: Qt.point(24,24)
        enableMotor: true
        frequencyHz: 10
    }

    WheelJoint {
        id: wheelJointB
        bodyA: body.body
        bodyB: wheelB.body
        localAnchorA: Qt.point(0,10)
        localAnchorB: Qt.point(24,24)
        enableMotor: true
        frequencyHz: 10
    }

    Rectangle {
        id: debugButton
        x: 50
        y: 50
        width: 120
        height: 30
        Text {
            text: "Debug view: " + (debugDraw.visible ? "on" : "off")
            anchors.centerIn: parent
        }
        color: "#DEDEDE"
        border.color: "#999"
        radius: 5
        MouseArea {
            anchors.fill: parent
            onClicked: debugDraw.visible = !debugDraw.visible;
        }
    }

    DebugDraw {
        id: debugDraw
        world: physicsWorld
        opacity: 0.5
        z: 1
        visible: false
    }
}
}
