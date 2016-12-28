import serial
import time
import MySQLdb #if not installed run 'sudo apt-get install python-mysqldb'

#connecting to database
db = MySQLdb.connect("localhost", "root", "", "co2_meter")
cursor = db.cursor()

ser = serial.Serial("/dev/ttyUSB0")
print "S8\n"
ser.flushInput()
time.sleep(1)

while(True):

    ser.flushInput()
    ser.write("\xFE\x44\x00\x08\x02\x9F\x25")
    time.sleep(.5)
    resp = ser.read(7)
    high = ord(resp[3])
    low = ord(resp[4])
    co2 = (high*256) + low

    #Inserting data into a database
    cursor.execute("INSERT INTO s8(co2) values(%s)",(co2))
    db.commit()

    print "CO2 = " +str(co2)
    time.sleep(300)
