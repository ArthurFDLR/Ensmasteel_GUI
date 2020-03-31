import serial
import time
import csv

TIME0 = time.time_ns()
Time_ms = lambda : int((time.time_ns()-TIME0) * 1e-6)
Time_ns = lambda : time.time_ns()-TIME0
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
        #print(line)
        recording = ((line == b'received ID 2\r\n') or (line == b'@Tirette|0\n')) # trigger signal
    if(Time_ms() - timeLast_ms > 8e2):
        print(".", end = '', flush=True)
        timeLast_ms = Time_ms()

## Record signal
print("\n\nStart recording :\n")
TIME0 = time.time_ns()
timeLast_ns = Time_ns()

with open("Bot_Telemetry.csv", "w", newline='') as f:
    writer = csv.writer(f,delimiter=";")
    while True:
        try:
            '''
            if(Time_ms() - timeLast_ms > 8e2):
                print(".")
                timeLast_ms = Time_ms()
            '''
            if(Ser_Recorded.inWaiting() > 0):
                line_bytes = Ser_Recorded.readline()
                timeLast_ns = Time_ns()
                line_str = line_bytes[0:len(line_bytes)-1].decode("utf-8")
                print(str(timeLast_ns) + " >> " + line_str)
                writer.writerow([timeLast_ns,line_str])
            
        except:
            print("Keyboard Interrupt")
            Ser_Recorded.close()
            break