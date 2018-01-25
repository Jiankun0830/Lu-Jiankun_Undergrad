import QtQuick 2.2
import Box2D 2.0
import QtQuick.Controls 1.1
import "shared"
import "components"

ApplicationWindow {
    visible: true
    width: 800
    height: 1000
    title: "Snap Chain"


Rectangle {
    id: screen

    width: 800
    height: 1000

    Rectangle{
        height: 500
        width: 700
        x:50
        y:250
        color: "#6CDACF"
    }

    Slider {
        id: lengthSlider
        x: 680
        y: 50
        width: 100
        height: 50
        maximumValue: 50
        minimumValue: 20
        value: 21
    }

    Component {
        id: shootball
        Rectangle {
            id: agentBall

            property color agentColor: "red"

            width: 20
            height: 20
            radius: 10
            color: agentColor
            border.color: "white"
            smooth: true

            property Body body: circleBody

            property int score: 0

            CircleBody {
                id: circleBody

                target: agentBall
                world: physicsWorld

                bullet: true
                bodyType: Body.Dynamic

                radius: agentBall.radius
                density: 1
                friction: 0
                restitution: 1
                gravityScale: 0
                fixture.onBeginContact: {
                  // for access of the collided entity and the entityType and entityId:
                  var body = other.getBody();
//                  var collidedEntity = body.target;
//                  var collidedEntityType = collidedEntity.entityType;
//                  var collidedEntityId = collidedEntity.entityId;
                  if (agentBall.y < 750 && agentBall.y > 250 && agentBall.x > 47 && agentBall.x < 735){
                      body.target.destroy();
                      if(agentBall.body.linearVelocity.y>0){
                          score1.score += 1;
                      }else{
                          score2.score += 1;
                      }
                  }

                }
            }
        }

    }

    Component {
        id: randomball
        PhysicsItem {
            id: ball

            width: 30
            height: 30

            bodyType: Body.Static
            world: physicsWorld

            gravityScale: 0

            property color color: "lightblue"

            fixtures:
                Circle {
                id:circle
                radius: ball.width / 2
                density: 0
                restitution: 1
            }

            Rectangle {
                radius: parent.width / 2
                border.color: "white"
                color: parent.color
                width: parent.width
                height: parent.height
                smooth: true
            }
        }
    }

    Component {
        id: linkComponent
        PhysicsItem {
            id: ball

            width: 20
            height: 20

            bodyType: Body.Dynamic
            world: physicsWorld

            gravityScale: 0

            property color color: "#EFEFEF"

            fixtures:
                Circle {
                id:circle
                radius: ball.width / 2
                density: 0.5
                restitution: 0
            }

            Rectangle {
                radius: parent.width / 2
                border.color: "blue"
                color: parent.color
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
    }

    Component {
        id: jointComponent
        RopeJoint {
            localAnchorA: Qt.point(10,10)
            localAnchorB: Qt.point(10,10)
            maxLength: lengthSlider.value
            collideConnected: true
        }
    }

    World { id: physicsWorld }

    Component.onCompleted: {
        var prev = leftWall;
        for (var i = 60;i < 740;i += 20) {
            var newLink = linkComponent.createObject(screen);
            newLink.color = "orange";
            newLink.x = i;
            newLink.y = 100;
            var newJoint = jointComponent.createObject(screen);
            if (i === 60)
                newJoint.localAnchorA = Qt.point(40, 100);
            newJoint.bodyA = prev.body;
            newJoint.bodyB = newLink.body;
            prev = newLink;
        }
        newJoint = jointComponent.createObject(screen);
        newJoint.localAnchorB = Qt.point(0,100);
        newJoint.bodyA = prev.body;
        newJoint.bodyB = rightWall.body;

        var prev = leftWall;
        for (var i = 60;i < 740;i += 20) {
            var newLink = linkComponent.createObject(screen);
            newLink.color = "orange";
            newLink.x = i;
            newLink.y = 900;
            var newJoint = jointComponent.createObject(screen);
            if (i === 60)
                newJoint.localAnchorA = Qt.point(40, 900);
            newJoint.bodyA = prev.body;
            newJoint.bodyB = newLink.body;
            prev = newLink;
        }
        newJoint = jointComponent.createObject(screen);
        newJoint.localAnchorB = Qt.point(0,900);
        newJoint.bodyA = prev.body;
        newJoint.bodyB = rightWall.body;
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

    Wall {
        id: topWall
        height: 40
        anchors {
            left: parent.left
            right: parent.right
            top: parent.top
        }
    }

    Wall {
        id: leftWall
        width: 40
        anchors {
            left: parent.left
            top: parent.top
            bottom: parent.bottom
            bottomMargin: 40
        }
    }

    Wall {
        id: rightWall
        width: 40
        anchors {
            right: parent.right
            top: parent.top
            bottom: parent.bottom
            bottomMargin: 40
        }
    }



    Timer {
        id: ballsTimer
        interval: 500
        running: true
        repeat: false // set this to true to get unlimited balls dropping
        onTriggered: {
            var newBox = shootball.createObject(screen);
            newBox.x = 100 + (Math.random() * (screen.width - 200));
            newBox.y = 120;
        }
    }

    Timer {
        id: ballsTimer2
        interval: 5000
        running: true
        repeat: true // set this to true to get unlimited balls dropping
        onTriggered: {
            var newBox = randomball.createObject(screen);
            newBox.x = 50 + (Math.random() * (screen.width - 120));
            newBox.y = 250 + (Math.random() * (screen.height-500));
        }
    }

    Text{
        property int score: 0
        id:score1
        x:50
        y:50
        text: "Player 1: " + score
        font.family: "Helvetica"
        font.pointSize: 24
    }
    Text{
        property int score: 0
        id:score2
        x:600
        y:950
        text: "Player 2: " + score
        font.family: "Helvetica"
        font.pointSize: 24
    }
}
}
