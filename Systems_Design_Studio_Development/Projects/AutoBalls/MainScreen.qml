import QtQuick 2.7
import QtQuick.Controls 1.2
import QtQuick.Controls.Styles 1.2
import QtQuick.Layouts 1.0

import Box2D 2.0  //There should be a directory called Box2D in the qml directory of your Qt installation.

import "boxes" as QtBoxes //boxes is a subdirectory of this project; we rename it as "QtBoxes"

//Everything on the main screen lives withing a rectangle
Rectangle{
            id: worldContainer
            anchors.fill: parent   // the rectangle will fill the parent window (see main.qml)

            ListModel{      // this is a list to define how many balls there will be and what their initial state will be.
                            // A repeater function in the Balls.qml component (see below) will use this list to create the balls.

                id: agents  // We call this list agents because the balls will have their own logic to follow, like independent agents.

                // The list consists of ListElements. There are three ListElements, so there will be three balls created.

                ListElement {      //We define each list element to hold four pieces of data: an id for the agent, its initial X location, Y locations,
                                    // and the index of the first waypoint to aim for.
                    agentID: "e1"
                    initialX: 100
                    initialY: 400
                    //agentcolor:""
                    firstWaypoint: 6

                }

                ListElement {
                    agentID: "e2"
                    initialX: 273.2
                    initialY: 500
                    //agentcolor:""
                    firstWaypoint: 1

                }
                ListElement {
                    agentID: "e3"
                    initialX: 446.4
                    initialY: 400
                    //agentcolor:""
                    firstWaypoint: 2

                }
                ListElement {
                    agentID: "e4"
                    initialX: 446.4
                    initialY: 200
                    //agentcolor:""
                    firstWaypoint: 3

                }
                ListElement {
                    agentID: "e5"
                    initialX: 273.2
                    initialY: 100
                    //agentcolor:""
                    firstWaypoint: 4

                }
                ListElement {
                    agentID: "e6"
                    initialX: 100
                    initialY: 200
                    //agentcolor:""
                    firstWaypoint: 5

                }



                // Go ahead and add more elements to this list. Be sure to give them unique initialX and initialY values
            }
            ListModel{  //This is a list of waypoints to manage the movement of the balls. The idea is that when a ball reaches one waypoint,
                        // we will assign it the next waypoint to move towards. The agent will travel in straight lines between waypoints.
                        // An alternative would be to describe a grid of points.

                id:waypoints  //We refer to this list by the name "waypoints"

                ListElement{  //We define each list element to hold three pieces of data: an id, an x location, and a y location
                    wayID:1
                    x: 100
                    y:200
                    elementcolor:"lightgreen"
                }
                ListElement{
                    wayID:2
                    x: 100
                    y:400
                    elementcolor:"lightblue"
                }
                ListElement{
                    wayID:3
                    x: 273.2
                    y:500
                    elementcolor:"yellow"
                }
                ListElement{
                    wayID:4
                    x: 446.4
                    y:400
                    elementcolor:"red"
                }
                ListElement{
                    wayID:5
                    x: 446.4
                    y:200
                    elementcolor:"pink"
                }
                ListElement{
                    wayID:6
                    x: 273.2
                    y:100
                    elementcolor:"orange"
                }
            }


            World {                 // All the Box2D elements must be created to belong to a Box2D World. Here we define the world.
                id: physicsWorld    // Our name for the world is "physicsWorld"
                                    // There is nothing in the World to start with except a definition of how to handle the World's Stepped event.
                                    // The Stepped event is a clock tick function: every tick of the clock, the Stepped event is triggered
                onStepped: {
                        // this is how we do agent-based simulation
                        // Every tick of the clock we can check the status of our agents (the balls) and adjust their behavior
                        // We will implement a simple behavior: for each agent we will compare its location to the waypoint it is heading toward.
                        // If it is close to waypoint we will pick a new waypoint for it to move toward.
                        // Knowing the waypoint the ball should be heading towards, we will adjust the velocity of the
                        // ball to aim for that point at a constant speed.
                        //
                        // The behavior is described using javascript code.
                        var i;
                        for (i=0;i<agents.count;i++){
                            //get the ball with index i
                            var tbody = balls.agentRepeater.itemAt(i).agent.body;
                            var nextWaypoint = balls.agentRepeater.itemAt(i).agent.nextWaypoint;
                            // assign a dummy target (this will be overwritten once we access the waypoint)
                            var target = Qt.point(0,0);
                            // find the waypoint in the list of waypoints
                            for(var j = 0; j < waypoints.count; j++) {
                              var waypoint = waypoints.get(j);
                                // we are matching waypoints based on the wayID attribute.
                                // That way you could have waypoints with id's like "Home", "Office", "School" to help you remember where they are.
                              if(nextWaypoint == waypoint.wayID) {
                                target = Qt.point(waypoint.x,waypoint.y)
                                balls.agentRepeater.itemAt(i).agent.agentColor = waypoint.elementcolor
                              }
                            }
                            // By now we have a real target for this agent
                            // get the current location of this agent
                            var currentLocation = tbody.getWorldCenter();
                            // get a vector pointing toward the target
                            var direction = Qt.point(target.x-currentLocation.x,target.y-currentLocation.y);
                            //normalize the direction
                            var r = Math.sqrt(Math.pow(direction.x,2)+Math.pow(direction.y,2));
                            // if r is small, pick a new waypoint
                            if (r<1 ){
                                // Here I am assuming the wayID's are all numbers between 1 and the number of waypoints
                                nextWaypoint = nextWaypoint+1; //a crazy rule just to make things interesting
                                if (nextWaypoint>waypoints.count)nextWaypoint = 1; // make sure the nextWaypoint is possible
                                //set the next waypoint for this agent
                                balls.agentRepeater.itemAt(i).agent.nextWaypoint= nextWaypoint;
                            }

                            direction.x = direction.x/r;
                            direction.y = direction.y/r;

                            // set the desired speed to whatever you like
                            var desiredSpeed = 4;
                            // scale the normalized direction by the desired speed to get the desired velocity
                            var desiredVelocity =Qt.point(desiredSpeed*direction.x,desiredSpeed*direction.y);

                           //console.log("x "+tbody.linearVelocity.x+" y "+tbody.linearVelocity.y);

                            // set the linear velocity of this agent
                            tbody.linearVelocity.x= desiredVelocity.x;
                            tbody.linearVelocity.y= desiredVelocity.y;
                        }
                    }
            }
            // We have created a component called Balls: it is in the boxes sub-directory. We aliased "boxes" to QtBoxes up above.
            // The Balls component has several properties that we can access (id, physicsWorld, and agentList.
            // Open the Balls.qml file next to see what it does.
            QtBoxes.Balls{
                    id: balls
                    physicsWorld: physicsWorld
                    agentList: agents            // Here is where we pass the list of agents to be created. The list is defined above.
            }

}

