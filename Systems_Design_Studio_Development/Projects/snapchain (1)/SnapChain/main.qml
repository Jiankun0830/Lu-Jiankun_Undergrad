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

    MultiPointTouchArea{
        anchors.fill: parent
        touchPoints: [
            TouchPoint { id: point1 },
            TouchPoint { id: point2 }
        ]
    }

    Rectangle{
        height: 300
        width: 700
        x:50
        y:350
        color: "#6CDACF"
    }

    Shootball{
        id:shootball
        x:300
        y:400
    }


    Component {
        id: randomball
        Randomball{}
    }

    Component {
        id: linkComponent
        Dragball{}
    }

    Component{
        id: linkComponent1
        Chainball{}
    }

    Component {
        id: jointComponent
        RopeJoint {
            localAnchorA: Qt.point(10,10)
            localAnchorB: Qt.point(10,10)
            maxLength: 18
            collideConnected: true
        }
    }

    World { id: physicsWorld }

    Component.onCompleted: {
        var prev = leftWall;
        for (var i = 60;i < 740;i += 15) {
            if (i == 300 | i == 495){
                var newLink = linkComponent.createObject(screen);
            }else{
                var newLink = linkComponent1.createObject(screen);
            }
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
        for (var i = 60;i < 740;i += 15) {
            if (i == 300 | i == 495){
                var newLink = linkComponent.createObject(screen);
            }else{
                var newLink = linkComponent1.createObject(screen);
            }
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
        id: ballsTimer2
        interval: 2500
        running: true
        repeat: true // set this to true to get unlimited balls dropping
        onTriggered: {
            var newBox = randomball.createObject(screen);
            newBox.x = 80 + (Math.random() * 600);
            newBox.y = 350 + (Math.random() * (screen.height-700));
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

    Button{
        x:50
        y:970
        text: "GO"
        onClicked: {
            shootball.accelerate();
        }
    }
}
}
