import time
import serial


ser = serial.Serial(
    port='/dev/ttyUSB1',	#Configurar con el puerto
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

ser.isOpen()
ser.timeout=None
print(ser.timeout)

print ('Ingrese un comando:[0,1,2,3]\r\n')

while 1 :
    inputData = input("<< ")
    if inputData == 'exit':
        ser.close()
        exit()
    elif(input == '3'):
        print ("Wait Input Data")
        ser.write(inputData.encode())
        time.sleep(2)
        readData = ser.read(1)
        out = readData.decode()
        print(ser.inWaiting())
        if out != '':
            print (">>" + out)
    else:
        ser.write(inputData.encode())
        time.sleep(1)
