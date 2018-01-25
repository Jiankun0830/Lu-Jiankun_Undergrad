import QtQuick 2.2
import Box2D 2.0
import QtQuick.Controls 1.1
import "shared"

Rectangle {
    id: agentBall

    property color agentColor: "red"

    width: 30
    height: 30
    radius: 15
    color: agentColor
    border.color: "white"
    smooth: true

    property Body body: circleBody

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

              agentBall.destroy();
          }

    }

    Image{
        source: "images/pig.png"
        height: 40
        width:40
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter
    }

    function accelerate(){
        var vel_y = agentBall.body.linearVelocity.y
        if ( vel_y < 5 & vel_y >= 0){
            agentBall.body.linearVelocity.y = 5 + Math.random()*3;
            agentBall.body.linearVelocity.x = Math.random()*3
        }else if (vel_y > -5 & vel_y < 0){
            agentBall.body.linearVelocity.y = -(5 + Math.random()*3);
            agentBall.body.linearVelocity.x = Math.random()*3

        }
    }
}
