# Initialize two paired com port with com0com (or other virtual port emulator) : https://sourceforge.net/projects/com0com/

import time
import serial
import atexit

ser1 = serial.Serial(
    port='COM6',
    baudrate=9600,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)

ser2 = serial.Serial(
    port='COM7',
    baudrate=9600,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)

ser1.isOpen()
ser2.isOpen()

print("Started")

while(True):
    ser1.write(str.encode('Hello ser2, I am ser1 !'))
    print('ser1 >> Hello ser2, I am ser1 !')

    out = ''
    time.sleep(1)
    while ser2.inWaiting() > 0:
        out += ser2.read(1).decode("utf-8")
    if out != '':
        print("ser2 <<" + out)
    else:
        print("Error")
    

def exit_handler():
    print("Close communication")
    ser1.close()
    ser2.close()

atexit.register(exit_handler)