import QtQuick 2.2
import Box2D 2.0
import "../shared"

PhysicsItem {
    id: wall

    fixtures: Box {
        width: wall.width
        height: wall.height
        friction: 0
        density: 1
        restitution: 1
    }

    Image {
        source: "../images/wall.jpg"
        fillMode: Image.Tile
        anchors.fill: parent
    }
}
