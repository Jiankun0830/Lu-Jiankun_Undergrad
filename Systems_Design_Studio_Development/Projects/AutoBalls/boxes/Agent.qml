import QtQuick 2.0
import Box2D 2.0   //We refer to Body.Dynamic which is defined in Box2D
import "../shared"  //CircleBody is defined in the shared folder

Rectangle {
    id: agentBall

    property color agentColor: "white"

    width: 40
    height: 40
    radius: 20
    color: agentColor
    border.color: "black"
    smooth: true

    property Body body: circleBody
    property alias agentText: agentText.text
    property int  nextWaypoint

    CircleBody {
        id: circleBody

        target: agentBall
        world: physicsWorld

        bullet: true
        bodyType: Body.Dynamic

        radius: agentBall.radius
        density: 0.9
        friction: 0.9
        restitution: 0.2
    }
    Text{
        id:agentText
        x:15
        y:10
    }


}


