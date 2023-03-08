import time
import serial
import sys
import binascii 

high_byte_red   = b'\x02' 
low_byte_red    = b'\x49'

high_byte_blue  = b'\x04'
low_byte_blue   = b'\x92'

high_byte_green = b'\x09'
low_byte_green  = b'\x24'

high_byte_state = b'\x00' 
low_byte_state  = b'\x01'

portUSB = sys.argv[1]

ser = serial.Serial(
    port='/dev/ttyUSB{}'.format(int(portUSB)),	#Configurar con el puerto
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

ser.isOpen()
ser.timeout=None
print(ser.timeout)

#Codificacion
def Codificacion(byte_high, byte_low, dispositivo):

    data = byte_high+byte_low

    # print(data)
    if (len(data)<=15):
        cabecera = binascii.unhexlify(str(hex(0xA0+eval(hex(len(data))))).split("0x")[1])
        high = b'\x00'
        low  = b'\x00'
        dispo = binascii.unhexlify(dispositivo)
        cola = binascii.unhexlify(str(hex(0x40+eval(hex(len(data))))).split("0x")[1])
        
        Hex_trama = cabecera + high + low + dispo + data + cola

        # print("Trama corta en Hex: ", Hex_trama)
        trama_list = list(Hex_trama)

    if (len(data)>15):
        data = byte_high+byte_low
        cabecera = b'\xB0'
        cola = b'\x50'
        high = b'\x01'
        low  = b'\xff' 
        dispo = binascii.unhexlify(dispositivo)

        Hex_trama_large = cabecera + high + low + dispo + data + cola

        # print("Trama larga en Hex: ", Hex_trama_large)
        trama_list = list(Hex_trama_large)
        
    return trama_list
#___________________Fin de Codificacion


print("|_______________________________________________________________|")
print("|_____________________PUERTO SERIE para FPGA____________________|")
print("|Ingrese una de las siguientes opciones                         |")
print("|OPCION ( rojo  ): Prende los led de color Rojo                 |")
print("|OPCION ( azul  ): Prende los led de color azul                 |")
print("|OPCION ( verde ): Prende los led de color verde                |")
print("|OPCION ( estado): devuelve el estado de salida de los switch's |")
print("|OPCION ( exit  ): Finaliza el programa                         |")
print("|_______________________________________________________________|")
print()

dispositivo = '01'
out = ''
while 1 :

    inputData = input("Opcion: ")

    if (inputData == 'exit'):
        ser.close()
        exit()

    # elif(inputData == '3'):
    #     print ("Wait Input Data")
    #     ser.write(inputData.encode())
    #     time.sleep(2)
    #     readData = ser.read(1)
    #     out = str(int.from_bytes(readData,byteorder='big'))
    #     print(ser.inWaiting())
    #     if out != '':
    #         print ("Salida de puertos: " + out)

    else:
        if (inputData == 'rojo'  ): 
            trama = Codificacion(high_byte_red,low_byte_red, dispositivo) 
            ser.write(trama)
        if (inputData == 'azul'  ): 
            trama = Codificacion(high_byte_blue,low_byte_blue, dispositivo)
            ser.write(trama)
        if (inputData == 'verde' ): 
            trama = Codificacion(high_byte_green,low_byte_green, dispositivo)
            ser.write(trama)
        if (inputData == 'estado'): 
            trama = Codificacion(high_byte_state,low_byte_state, dispositivo)
            ser.write(trama)
            time.sleep(2)

            while (ser.inWaiting() > 0):
                readData = ser.read(1)  
                out = str(int.from_bytes(readData,byteorder='big'))
            if out != '':
                print ("Salida de puertos: ", out)      
        time.sleep(1)
