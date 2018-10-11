import serial
import time
import numpy as np
from firebase import firebase
import pickle
import json
import RPi.GPIO as GPIO
import Adafruit_DHT

###firebase setup
url = "https://dw-1d-cc5-grp08.firebaseio.com/" # URL to Firebase database
token = "yurddml214RsOPi9Ua0OhuDgeuzxm2Q7v7V6T6ZZ" # unique token used for authentication
firebase = firebase.FirebaseApplication(url, token)

### get the data for machine learning
### define the functions for machine learning
mydata = open("Planty_database.json", "r")
bunchobject = json.loads(mydata.readline())
mydata.close()
for i in bunchobject:
    bunchobject[i] = np.array(bunchobject[i])
feature_list = range(3)
data = bunchobject['data'][:, feature_list]

def normalize_minmax(test,data = data):
    """
    a function that takes in two numpy arrays, normalize the first numpy array
    using the min/max normalization based on the second array and returns the normalized array.
    """

    size = data.shape
    if (len(size) == 1):
        columns = 1
    else:
        columns = size[1]
    for i in range(columns):
        maximum = np.max(data[:, i])
        minimum = np.min(data[:, i])
        denominator = maximum - minimum
        test[:, i] = (test[:, i] - minimum) / denominator
        data[:, i] = (data[:, i] - minimum) / denominator

    return test


###define the functions to get readings from sensors, and send command to water pump
def get_humidity_temperature():
   RH, T = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4) #4 refers to GPIO 4 on the RPi
   return RH, T

def get_moisture(ser):
    line = 0
    while not line:
        line = ser.readline()
    #to avoid error caused by the delay of reading from sensor at the begining
    moisture = 1023 - float(line[-4:])  # to avoid error caused by multiple reading from hunidity sensor
    return moisture

def water_pump(ser,command):
    if command:
        ser.write(b"True")
        return True
    else:
        ser.write(b'False')
        return False


if __name__ == '__main__':
    #    main program that applying machine learning to decide whether to water or not and send data to the firebase database
    # change the port's name to the correct serial port, the port is used to send command to water pump and read from moisture sensor.
    ser = serial.Serial('/dev/ttyUSB0',38400,timeout=0.05)
    features = range(3)
    file = open('model.pickle', 'rb')
    model = pickle.load(file)
    file.close()
    while True:
        realtime_data_humidity = firebase.get('/humidity')
        realtime_data_temperature = firebase.get('/temperature')
        realtime_data_moisture = firebase.get('/moisture')# get the current data from firebase
        watering_records = firebase.get('/watering_records')
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        moisture = get_moisture(ser)
        humidity, temperature = get_humidity_temperature()
        print(moisture,humidity,temperature)
        real_time_data = normalize_minmax(np.array([[moisture,humidity,temperature]]))
        result = model.predict(real_time_data)
        water_pump(ser,result[0])
        if result[0]:
            watering_records.append(current_time)
            firebase.put('/','watering_records',watering_records)
        realtime_data_temperature[current_time] = temperature
        realtime_data_moisture[current_time] = moisture
        realtime_data_humidity[current_time] = humidity
        firebase.put('/', 'humidity', realtime_data_humidity)
        firebase.put('/', 'temperature', realtime_data_temperature)
        firebase.put('/', 'moisture', realtime_data_moisture)  # update the data on firebase



