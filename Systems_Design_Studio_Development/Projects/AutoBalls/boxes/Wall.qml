import QtQuick 2.0
import "../shared"  // BoxBody is defined in the shared folder

Item {
    id: wall

    BoxBody {
        target: wall
        world: physicsWorld  //physicsWorld is not declared as a property so it must be defined by the containing object

        width: wall.width
        height: wall.height
    }
}
