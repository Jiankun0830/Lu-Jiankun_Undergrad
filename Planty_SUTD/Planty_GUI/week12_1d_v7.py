# This is the 7th version of SmartGardener App for DW 1D Project by Group 8
# The corresponding kv file: SmartGardenerNeo.kv
# import basic modules
import time, datetime
import numpy as np
from firebase import firebase
import matplotlib
from matplotlib import pyplot as plt
# import modules related to kivy
from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
# define global variables just for testing
url = "https://dw-1d-cc5-grp08.firebaseio.com/" # can be changed
token = "yurddml214RsOPi9Ua0OhuDgeuzxm2Q7v7V6T6ZZ" # can be changed
# configure the window as the size of mobile screen
Config.set('graphics', 'height', '500')
Config.set('graphics', 'width', '250')
Config.set('graphics', 'fullscreen', 0)
# change the font size in matplotlib
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 20}
matplotlib.rc('font', **font)
# access the data from firebase
database = firebase.FirebaseApplication(url, token)
time_data = list(database.get('/humidity'))
hum_data = list(database.get('/humidity').values())
moi_data = list(database.get('/moisture').values())
temp_data = list(database.get('/temperature').values())
water_data = database.get('/watering_records')
# update the latest values and use for the widgets
last_update_raw = time_data[-1]
time_str = datetime.datetime.strptime(last_update_raw, '%Y-%m-%d %H:%M:%S')
temperature = "{:4.1f}°C".format(temp_data[-1])
humidity = '{:4.1f}% RH'.format(hum_data[-1])
moisture = '{:4.1f}'.format(moi_data[-1])
# prepare the watering data for watering frequency information
try:
    five_water_raw = water_data[-5:]
except IndexError:                           # in case there is not enough data in firebase
    five_water_raw = water_data
five_water = list(datetime.datetime.strptime(w, '%Y-%m-%d %H:%M:%S') for w in five_water_raw)
intervals = [five_water[n+1]-five_water[n] for n in range(len(five_water)-1)]  # should get 4 timedelta objects
frequency_raw = np.mean(intervals)           # calculate the numeric average of the watering frequency
time_str = five_water[-1]                    # this is the later watering record
last_water = time_str.strftime('%b %d %H:%M')
time_next_num = time_str+frequency_raw-datetime.datetime.now()
time_next = str(time_next_num.days*24+frequency_raw.seconds//3600) + ' hours later' # make prediction based on the past


class Main(FloatLayout):                           # define a separate class for easier reference in kv file
    def __init__(self, **kwargs):
        self.time = str(time.strftime('%I:%M%p'))
        Builder.load_file('SmartGardenerNeo.kv')   # load the kv file to set the layout
        self.temp = temperature
        self.hum = humidity
        self.moi = moisture
        self.last_water = last_water
        self.time_next = time_next
        self.rank = str(int(round(float(self.hum[:-5]) / 20, 0)))
        self.freq = 'Every ' + str(frequency_raw.days*24+frequency_raw.seconds//3600) + ' hours'
        time_arr = list(datetime.datetime.strptime(
            time, '%Y-%m-%d %H:%M:%S').strftime('%H:%M') for time in time_data)
        self.fig = plt.figure()
        try:
            plt.plot(np.array(time_arr)[-30::5], np.array(moi_data)[-30::5], 'k-', linewidth=2.0)
        except IndexError:
            plt.plot(np.array(time_arr), np.array(moi_data), 'w-', linewidth=2.0)
        #plt.xlabel('time')
        #plt.ylabel('moisture')                    # these two lines not shown because of limited space on GUI
        plt.title('Real-time Moisture')
        plt.ylim((0, 1200))
        plt.savefig("graph.png", transparent=True)
        super(Main, self).__init__(**kwargs)
        Clock.schedule_interval(self.reload, 10)   # update the data every 10 seconds automatically

    def reload(self, dt=10):
        # re-calculate all the global quantities
        frequency_num = 24  # this needs to be modified
        database = firebase.FirebaseApplication(url, token)
        time_data = list(database.get('/humidity'))
        hum_data = list(database.get('/humidity').values())
        moi_data = list(database.get('/moisture').values())
        temp_data = list(database.get('/temperature').values())
        water_data = database.get('/watering_records')
        temperature = "{:4.1f}°C".format(temp_data[-1])
        humidity = '{:4.1f}% RH'.format(hum_data[-1])
        moisture = '{:4.1f}'.format(moi_data[-1])
        try:
            five_water_raw = water_data[-5:]
        except IndexError:
            five_water_raw = water_data
        five_water = list(datetime.datetime.strptime(w, '%Y-%m-%d %H:%M:%S') for w in five_water_raw)
        intervals = [five_water[n + 1] - five_water[n] for n in range(len(five_water) - 1)]
        frequency_raw = np.mean(intervals)
        time_str = five_water[-1]
        last_water = time_str.strftime('%b %d %H:%M')
        time_next_num = time_str + frequency_raw - datetime.datetime.now()
        time_next = str(time_next_num.days * 24 + frequency_raw.seconds // 3600) + ' hours later'
        # pass the global quantities to class attributes
        self.ids.time.text = str(time.strftime('%I:%M%p'))
        self.ids.temp_val.text = temperature
        self.ids.hum_val.text = humidity
        self.ids.moi_val.text = moisture
        self.ids.lastW_val.text = last_water
        self.ids.nextW_val.text = time_next
        self.rank = str(int(round(float(self.hum[:-5]) / 20, 0)))
        self.ids.cond_val.text = self.rank + '/5'
        self.freq = 'Every ' + str(frequency_raw.days*24+frequency_raw.seconds//3600) + ' hours'
        self.ids.freq_val.text = self.freq
        # update the graph
        time_arr = list(datetime.datetime.strptime(
            time, '%Y-%m-%d %H:%M:%S').strftime('%H:%M') for time in time_data)
        plt.gca().clear()
        try:
            plt.plot(np.array(time_arr)[-30::5], np.array(moi_data)[-30::5], 'k-', linewidth=2.0)
        except IndexError:
            plt.plot(np.array(time_arr), np.array(moi_data), 'w-', linewidth=2.0)

        #plt.xlabel('time')
        #plt.ylabel('moisture')                 # these two lines not shown because of limited space on GUI
        plt.title('Real-time Moisture')
        plt.ylim((0, 1200))
        self.fig.savefig('graph.png', transparent=True)
        self.ids.graph.source = 'graph.png'      # update the graph based on  the new plot saved

    def quit(self):
        App.get_running_app().stop()

class SmartGardener(App):
    def build(self):
        return Main()

if __name__ == '__main__':
    SmartGardener().run()
