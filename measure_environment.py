#!/usr/bin/python3
import configparser
import datetime
import mysql.connector
import socket
import time
from sense_emu import SenseHat

config = configparser.ConfigParser()
config['DEFAULT'] = {
    'username': 'myuser',
    'password': 'mypass123',
    'host': '10.64.80.65',
    'database': 'sensehat'    
}
config.read('measure_environment.ini')

sense = SenseHat()
sense.clear()

class Data:
    """Data from the SenseHat"""
    def __init__(self, sensehat):
        self.sensor = socket.gethostname()
        self.timestamp = datetime.datetime.utcnow().isoformat(' ')
        self.humidity = sensehat.get_humidity()
        self.temperature_from_humidity = sensehat.get_temperature_from_humidity()
        self.temperature_from_pressure = sensehat.get_temperature_from_pressure()
        self.pressure = sensehat.get_pressure()
        self.orientation = sensehat.get_orientation_radians()
        self.compass = sensehat.get_compass_raw()
        self.gyroscope = sensehat.get_gyroscope_raw()
        self.accelerometer = sensehat.get_accelerometer_raw()

    def sql_fields(self):
        result = "("
        result += "time, sensor, humidity, pressure"
        result += ", temperature_from_humidity, temperature_from_pressure"
        result += ", orientation_pitch, orientation_roll, orientation_yaw"
        result += ", compass_x, compass_y, compass_z"
        result += ", gyroscope_pitch, gyroscope_roll, gyroscope_yaw"
        result += ", accelerometer_pitch, accelerometer_roll, accelerometer_yaw"
        result += ")"
        return result;

    def to_sql(self):
        result = "("
        result += "'" + self.timestamp + "', '" + self.sensor + "', " + str(self.humidity) + ", " + str(self.pressure)
        result += ", " + str(self.temperature_from_humidity) + ", " + str(self.temperature_from_pressure)
        result += ", " + str(self.orientation["pitch"]) + ", " + str(self.orientation["roll"]) + ", " + str(self.orientation["yaw"])
        result += ", " + str(self.compass["x"]) + ", " + str(self.compass["y"]) + ", " + str(self.compass["z"])
        result += ", " + str(self.gyroscope["x"]) + ", " + str(self.gyroscope["y"]) + ", " + str(self.gyroscope["z"])
        result += ", " + str(self.accelerometer["x"]) + ", " + str(self.accelerometer["y"]) + ", " + str(self.accelerometer["z"])
        result += ")"
        return result
        
    def __str__(self):
        result = "Sensor: %s\n" % self.sensor
        result += "Timestamp: %s\n" % self.timestamp
        result += "Humidity: %s %%rH\n" % self.humidity
        result += "Temperature: %s C\n" % self.temperature_from_humidity
        result += "Temperature: %s C\n" % self.temperature_from_pressure
        result += "Pressure: %s Millibars\n" % self.pressure
        result += "Orientation p: {pitch}, r: {roll}, y: {yaw}\n".format(**self.orientation)
        result += "Compass x: {x}, y: {y}, z: {z}\n".format(**self.compass)
        result += "Gyroscope x: {x}, y: {y}, z: {z}\n".format(**self.gyroscope)
        result += "Accelerometer x: {x}, y: {y}, z: {z}\n".format(**self.accelerometer)
        return result



for x in range(5):
    data = Data(sense)
    print(data)
    statement = "INSERT INTO envdata" + data.sql_fields()
    statement += " VALUES" + data.to_sql()
    data = Data(sense)
    statement += ", " + data.to_sql()
    print(data)
    print("")
    print(statement)
    print("")
    print("Connectinng to server")
    ctx = mysql.connector.connect(user=config['DEFAULT']['username'],
                              password=config['DEFAULT']['password'],
                              host =config['DEFAULT']['host'],
                              database=config['DEFAULT']['database'])
    cursor = ctx.cursor()
    print("Inserting data")
    cursor.execute(statement)
    print("Commiting")
    ctx.commit()
    print("Closing")
    cursor.close()
    ctx.close();
    time.sleep(60)