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

    property int score: 0

    property int player: 0

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
          console.log(agentBall.x)
          if (agentBall.y < 350 && agentBall.y > 0 && agentBall.x > 50 && agentBall.x < 720){
             agentBall.player= 0;
          }
          if (agentBall.y < 1000 && agentBall.y > 650 && agentBall.x > 50 && agentBall.x < 720){
             agentBall.player= 1;
          }
          if (agentBall.y < 650 && agentBall.y > 350 && agentBall.x > 50 && agentBall.x < 720){
              if(agentBall.player < 0.5){
                score1.score += 1;
              }
              else{
                score2.score += 1;
              }
              //body.target.destroy();
          }

        }
    }

    Image{
        source: "images/angrybird.png"
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
