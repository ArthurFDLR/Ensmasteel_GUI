import csv
import time
import serial

ser = serial.Serial(
    port='COM6',
    baudrate=115200,
)
ser.isOpen()

def Wait_Signal(id):
    ser.flushInput()
    while(True):
        if(ser.inWaiting() > 5):
            for i in range(4): ser.read()
            messageID = int.from_bytes(ser.read(), "big")
            ser.flushInput()
            print(messageID)
            if (messageID == id):
                return True

Time_ns = lambda : time.time_ns()-TIME0

Wait_Signal(2)
TIME0 = time.time_ns()
with open('.\Telemetry_Simulator\Bot_Telemetry.csv', newline='') as f:
    reader = csv.reader(f, delimiter=';')
    for row in reader:
        while (int(row[0]) > Time_ns()): pass #Wait to send message at the correct timestamp
        line = row[1] + '\n'
        ser.write(line.encode())
        print(str(row[0]) + " >> " + row[1])