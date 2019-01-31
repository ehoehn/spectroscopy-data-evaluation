import serial
import serial.tools.list_ports
import regex as re
import io
import sys
import datetime, time


ser = serial.Serial()
# print(ser)
ser.baudrate = 19200

fo = open("foo.txt", "w", encoding='utf-8')

for i in serial.tools.list_ports.comports():
    print(i)
# for j in serial.tools.list_ports.grep('.'):
#     print(j)

ser.port = 'COM5'

print(ser)
# with ser as open:
# print(ser.open())
ser.open()
print(ser.is_open)

print(ser.read(100))
# print(ser.read())
# ser.close()

# sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))




# https://stackoverflow.com/questions/13890935/does-pythons-time-time-return-the-local-or-utc-timestamp
# https://stackoverflow.com/questions/54438914/adding-a-duration-to-a-start-time-string-to-get-a-finish-time
# print(int.from_bytes(b'\x11', byteorder=sys.byteorder))#

duration = input('Bitte Messdauer eingeben [h:mm:ss] ')
if duration == '':
    duration = '0:00:02'
else:
    duration = int(duration)

ts = datetime.datetime.now()

for i in range(1000):
    i = ser.read()
    i = int.from_bytes(i, byteorder=sys.byteorder)
    tf = datetime.datetime.now()
    te = tf - ts
    #print(str(te).split('.'))
    if str(te).split('.')[0] == str(duration):
        break
    fo.write(str(te) + ';' + str(i) + '\n')
fo.close()




