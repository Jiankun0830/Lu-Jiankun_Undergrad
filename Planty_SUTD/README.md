# SUTD-Planty

This aim of the project is to allow for a system that reads the plant's health by getting information about the soil and its surroundings, waters the plant automatically and gives the plant owner information about the plant's health on a mobile application and the watering timings.

Details about the project can be found in the poster.

## Hardware setup:
Conect moisture sensor, adafruit DHT22 and water pump to the raspherry pi.

## Details about sensors:
https://learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging/software-install-updated  DHT 22
https://detail.tmall.com/item.htm?spm=a230r.1.14.6.5bbf24a8zOqyvb&id=41272850226&cm_id=140105335569ed55e27b&abbucket=14  Moisture Sensor

## Build the machine learning model:
A database is provided to build machine learning model. Run Machine_learning_model.py on the raspherry pi, it will save the model as model.pickle for machine learning and print the accuracy of the model. Usually, the accuracy should be very high (more than 0.98), if the accuracy is not satisfying enough, simply run a few more times and save the model with the best accuracy.
Our product is not limited to any particular type of plant, as long as there is a database of the plant¡¯s water requirements, it will work for any and all plant species.

## How to run:
After finishing the previous steps, run planty_model.py, and the device will automatically water the plants

## GUI:
This GUI consists of three screens: Home, Graph and Info. The interface looks simple and clear and all the real-time data is processed in the program that supports the GUI. The data and graph are auto-updated every 10 seconds so that users will get all the information about the plant as well as the predictions for the smart watering system easily.You can run the kivy GUI program on any device (not necessarily the raspherry pi, you can run it on mobile phone, laptop etc.)