import QtQuick 2.0
import Box2D 2.0  //We make reference to World, which is a Box2D class so we need to import the Box2D library


Rectangle {
    id: screen
    anchors.fill: parent
    color:'black'
    Image {
            id: background
            width:640
            height:640
            fillMode: Image.TileHorizontally
            smooth: true
            source: 'qrc:/timg.jpg'
        }

    //pass in reference to World from the outside
    property World physicsWorld

    // pass in a list of agents from the outside
    property ListModel agentList

    //provide an alias for the repeater to the outside
    property alias agentRepeater: agentRepeater

    // The Repeater is a powerful feature of Qt to create objects based on a list.
    // In this case we use the list of agents to create objects of type Item.
    // Item is composed of a component Agent which is defined in the file Agent.qml in the boxes subdirectory.
    // The component Agent has properties x,y, agentColor, nextWaypoint, and agentText which we can bind to
    // to the generic elements of the agentList (initialX, initialY, firstWaypoint, and agentID.)
    // Open the file Agent.qml to see what a generic agent in this World looks like.

    Repeater{
        id: agentRepeater
        model: agentList
        delegate: Item{
            property alias agent: agent

            Agent{
                id: agent
                //x: (initialX-75)/500*(screen.width-100)
                //y: initialY/300*(screen.height/3)
                x:initialX
                y:initialY
                agentColor: "white"
                nextWaypoint: firstWaypoint
                agentText: agentID
            }
        }
    }

    // We have created a component called Wall which is based on the Box2D Box. Here we use that component to build
    // bounding walls for our world.

    Wall {
        id: ground
        height: 20
        anchors { left: parent.left; right: parent.right; top: parent.bottom }
    }
    Wall {
        id: ceiling
        height: 20
        anchors { left: parent.left; right: parent.right; bottom: parent.top }
    }
    Wall {
        id: leftWall
        width: 20
        anchors { right: parent.left; bottom: ground.top; top: ceiling.bottom }
    }
    Wall {
        id: rightWall
        width: 20
        anchors { left: parent.right; bottom: ground.top; top: ceiling.bottom }
    }



}
