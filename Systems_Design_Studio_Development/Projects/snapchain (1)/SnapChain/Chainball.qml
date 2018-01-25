import QtQuick 2.0
import Box2D 2.0
import "shared"

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
        density: 1
        restitution: 0
    }

    Rectangle {
        radius: parent.width / 2
        border.color: "blue"
        color: parent.color
        width: parent.width
        height: parent.height
        smooth: true
    }

}
