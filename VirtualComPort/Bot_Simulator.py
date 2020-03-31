import serial
import time
import csv

TIME0 = time.time_ns()
Time_ms = lambda : (int) (time.time_ns()-TIME0) * 1e-6
timeLast_ms = Time_ms()

Ser_Recorded = serial.Serial(
    port='COM4',
    baudrate=115200,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)

## Wait for serial signal
Ser_Recorded.flushInput()
recording = False
print("Wait for signal ", end = '', flush=True) 
while not recording:
    line = ""
    if(Ser_Recorded.inWaiting() > 0):
        line = Ser_Recorded.readline()
        recording = (line == b'received ID 2\r\n') # trigger signal
    if(Time_ms() - timeLast_ms > 8e2):
        print(".", end = '', flush=True)
        timeLast_ms = Time_ms()

## Record signal
print("\n\nStart recording :\n")
TIME0 = time.time_ns()
timeLast_ms = Time_ms()

while True:
    try:
        if(Time_ms() - timeLast_ms > 8e2):
            print(".")
            timeLast_ms = Time_ms()
        '''
        ser_bytes = ser.readline()
        decoded_bytes = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
        print(decoded_bytes)
        with open("test_data.csv","a") as f:
            writer = csv.writer(f,delimiter=",")
            writer.writerow([time.time(),decoded_bytes])
        '''
    except:
        print("Keyboard Interrupt")
        Ser_Recorded.close()
        break