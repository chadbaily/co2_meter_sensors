#Author: Chad Baily
#Company: Co2 Meter
#Date of Creation: 12/08/2016
#System run on: linux
import serial
from datetime import datetime
import time
# Needed if you want to connect a MySQL Database
#import MySQLdb #if not installed run 'sudo apt-get install python-mysqldb'

#connecting to database, this part is optional. You must change the options to match your MySQL Database
# db = MySQLdb.connect("localhost", "root", "", "co2_meter")
# cursor = db.cursor()

#The serial port will need to be changed accordingly. It can be found by running 'dmesg | grep "tty"'
ser = serial.Serial("/dev/ttyUSB0")

print "Cozir Sensor"

ser.write("K 2\r\n")

ser.flushInput()

time.sleep(1)

while True:
    #Gathering the Co2 From the sensor
    ser.write("Z\r\n")
    co2 = ser.read(10)

    #Gathering the Humidity from the sensor
    ser.write("H\r\n")
    humidity = ser.read(10)

    #Gathering the Temperature from the seonsor
    ser.write("T\r\n")
    temp = ser.read(10)

    #Converting the C02 Into a float
    co2 = co2[:8]
    fltCo2 = int(co2[2:])

    #Congverting the Humidity into a float and a realtive %
    humidity = humidity[:8]
    fltHumidity = float(humidity[2:])/10

    #Converting the Temperature to degrees C
    temp = temp[:8]
    fltTemp = (float(temp[2:]) - 1000)/10

    #Datetime
    dateTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    #This is needed to stop the 1st reading that is incorrect
    if (fltCo2 > 0 and fltHumidity > 0 and fltTemp > 0):
        print "Temperature in *C : ", fltTemp, " \t Co2 : ", fltCo2, "\t\t %  Humidity : ", fltHumidity
        #Inserting data into a database
        # cursor.execute("INSERT INTO cozir(temperature, humidity, co2, date) values(%s, %s, %s, %s)",(fltTemp, fltHumidity, fltCo2, dateTime))
        # db.commit()

    

    #sleep for 5 Minutes
    time.sleep(3)
