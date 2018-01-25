import QtQuick 2.6
import QtQuick.Window 2.2
import QtQuick.Controls 2.0

ApplicationWindow{
    visible: true
    width: 640
    height: 480
    title: "Hello World"


    Rectangle {
        id: page
        width: 640; height: 480
        color: "lightgray"

        Text {
            id: helloText
            text: "Hello world!"
            y: 60
            //anchors.verticalCenter: page.verticalCenter
            anchors.horizontalCenter: page.horizontalCenter
            font.pointSize: 24
            font.bold: true

            MouseArea{
                id:mouseArea
                anchors.fill:parent
            }

            states:State{
                name:"down"
                when:mouseArea.pressed == true
                PropertyChanges {
                    target: helloText
                    y:240
                    rotation:180
                    color:"red"
                        }
                    }
            transitions: Transition {
                from: ""
                to: "down"
                reversible: true
                ParallelAnimation{

                    NumberAnimation {
                        properties: "y,rotation"
                        duration: 500
                        easing.type: Easing.InOutQuad
                    }

                    ColorAnimation {
                        duration: 500
                    }

            }
            }
        }
    }

    Grid{
        id:colorPicker
        x: 40
        y: 400
        //anchors.bottom: page.bottom
        //anchors.bottomMargin: 4
        rows: 2
        columns: 3
        spacing: 3

        Cell { cellColor: "red"; onClicked: helloText.color = cellColor }
        Cell { cellColor: "green"; onClicked: helloText.color = cellColor }
        Cell { cellColor: "blue"; onClicked: helloText.color = cellColor }
        Cell { cellColor: "yellow"; onClicked: helloText.color = cellColor }
        Cell { cellColor: "steelblue"; onClicked: helloText.color = cellColor }
        Cell { cellColor: "black"; onClicked: helloText.color = cellColor }
    }

}