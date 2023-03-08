###########################################################################
#   Autor: Juarez Daniel, Jose Gomez Lazarte
#   Año: 2023
#   Nombre: uart8.py para comunicacion entre FPGA y la PC
##########################################################################

import time
import serial
import sys
import binascii 
import csv

#___Comunicacion puerto Serie para la FPGA
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
################################

#code
enable = b'\x80'
opc_1  = b'\x00' 
opc_2  = b'\x01'
opc_3  = b'\x02'
opc_4  = b'\x03'
opc_5  = b'\x04'
opc_6  = b'\x05'
opc_7  = b'\x06'
##############################################

#___Funcion para guardado de los datos recolectados de los filtros___#
def GuardadoCSV(tramaI, tramaQ):

    archivo = open('DatosFiltroI.csv', '+w') #con +w si no existe el archivo se lo crea
    for i in range(len(tramaI)):
        archivo.write(str(tramaI[i]))
        archivo.write(',')
        
    print("Writing complete DatosFiltroI")
    archivo.close()

    archivo = open('DatosFiltroQ.csv', '+w') #con +w si no existe el archivo se lo crea
    for i in range(len(tramaQ)):
        archivo.write(str(tramaQ[i]))
        archivo.write(',')

    print("Writing complete DatosFiltroQ")
    print()
    print()
    archivo.close()

#___Funcion para corroborar las tramas de los bits y errores transmitidos asi como la de los filtros___#
def CorroboracionTrama(TramaOK):

    if (ord(TramaOK[0])== 164): OK = 1
    else:   OK = 0
    if (ord(TramaOK[1])== 0):   OK = 1
    else:   OK = 0
    if (ord(TramaOK[2])== 0):   OK = 1
    else:   OK = 0
    if (ord(TramaOK[3])== 1):   OK = 1
    else:   OK = 0   
    if (ord(TramaOK[8])== 68):  OK = 1
    else:   OK = 0

    return OK 

#___Funcion para armar la trama a enviar a la FPGA___#
def Codificacion(opc, sub_opc , dispositivo):

    data = opc + enable + b'\x00' + sub_opc
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

    # if (len(data)>15):
    #     dispo = opc + enable + b'\x00' + b'\x00' + b'\x00' + b'\x00' + sub_opc
    #     cabecera = b'\xB0'
    #     cola = b'\x50'
    #     high = b'\x01'
    #     low  = b'\xff' 
    #     dispo = binascii.unhexlify(dispositivo)

    #     Hex_trama_large = cabecera + high + low + dispo + data + cola

    #     print("Trama larga en Hex: ", Hex_trama_large)
    #     trama_list = list(Hex_trama_large)
        
    return trama_list 

#___Funcion para decodificar algun error en el envio de tramas hacia la FPGA___#
def Decodificacion(trama):

    #CODIFICANDO EL MENSAJE
    for i in range (1000):
        ser.write(trama)

    large = ser.inWaiting()
    cabecera = 4   
    read_data = []
    opc = ""

    while (ser.inWaiting() > 0):  
        read_data.append(chr(ord(ser.read(1))))

    opc = "".join(read_data[cabecera:large-1])
    print("mensaje recibido: ", opc)   
    print()
    print()

#___Funcion para decodificar los errores y bits transmitidos___#     
def DecoBitsAndErr(trama):

    #CODIFICANDO EL MENSAJE
    ser.write(trama)    
    time.sleep(1)    

    cabecera  =  4   
    count     =  0
    tramaok   =  0 
    read_data =  []
    tramaAux  =  []
    Btis_I    =  []
    Btis_Q    =  []
    Error_I   =  []
    Error_Q   =  []

    while (ser.inWaiting() > 0):  
        read_data.append(chr(ord(ser.read(1))))

    for i in range (8):
        for i in range (9):    
            tramaAux.append(read_data[count])
            count += 1
            
        tramaok = CorroboracionTrama(tramaAux)
        if(tramaok == 1): tramaAux.clear()
        else: 
            print("Error en la Trama : ",tramaAux )
            exit()

    low_B_tram_I  = "".join(read_data[(63+cabecera):(72-1)])
    High_B_tram_I = "".join(read_data[(54+cabecera):(63-1)])

    low_E_tram_I  = "".join(read_data[(45+cabecera):(54-1)])
    High_E_tram_I = "".join(read_data[(36+cabecera):(45-1)])

    low_B_tram_Q  = "".join(read_data[(27+cabecera):(36-1)])
    High_B_tram_Q = "".join(read_data[(18+cabecera):(27-1)])

    low_E_tram_Q  = "".join(read_data[(9+cabecera):(18-1)])
    High_E_tram_Q = "".join(read_data[(0+cabecera):(9-1)])       


    Bit_tram_I = High_B_tram_I + low_B_tram_I 
    Err_tram_I = High_E_tram_I + low_E_tram_I
    Bit_tram_Q = High_B_tram_Q + low_B_tram_Q
    Err_tram_Q = High_E_tram_Q + low_E_tram_Q    

    for i in range (len(Bit_tram_I)):
        Btis_I.append (str(ord(Bit_tram_I[i])))
        Error_I.append(str(ord(Err_tram_I[i])))        
        Btis_Q.append (str(ord(Bit_tram_Q[i])))
        Error_Q.append(str(ord(Err_tram_Q[i])))

    print("Bits transmitidos ( I ): ",    "".join(Btis_I) )
    print("Bits transmitidos ( Q ): ",    "".join(Btis_Q) )
    print("Errores transmitidos ( I ): ", "".join(Error_I))    
    print("Errores transmitidos ( Q ): ", "".join(Error_Q))
    print()
    print()

#___Funcion para decodificar los datos de los filtros___#
def DecoTramaBitQI(trama):

    ser.write(trama)    
    time.sleep(1)    

    cabecera  =  4   
    read_data =  []
    trama1 = []
    trama2 = []
    tramaQ = []
    tramaI = []
    Trama_Float_I = []
    Trama_Float_Q = []
 
    count = 0
    while (ser.inWaiting() > 0):  
        read_data.append(chr(ord(ser.read(1))))

    for i in range((len(read_data)//9)):            #Se obtiene las 900 tramas de 9 byte cada una
        for j in range(9): 
            trama1.append(read_data[(count)])
            count += 1
        tramaok = CorroboracionTrama(trama1)
        if(tramaok == 1): trama2 = trama1[cabecera:(len(trama1)-1)]
        else: 
            print("Error en la Trama : ",trama1 )
            exit()            

        auxQ = hex(ord(trama2[2])).split('0x')[1] #Obtenemos el dato en hexadecimal   
        auxI = hex(ord(trama2[0])).split('0x')[1]
       
        if (len(auxI) != 1):
            tramaI.append(int.from_bytes(binascii.unhexlify(auxI), byteorder="big", signed=True)) #Obtenemos el dato como entero con signo
        else:
            tramaI.append(int.from_bytes(binascii.unhexlify('0' + auxI), byteorder="big", signed=True))

        if (len(auxQ) != 1):
            tramaQ.append(int.from_bytes(binascii.unhexlify(auxQ), byteorder="big", signed=True)) 
        else: 
            tramaQ.append(int.from_bytes(binascii.unhexlify('0' + auxQ), byteorder="big", signed=True))        
        #____________________________________________________________________________________________#

        trama1.clear()     
        trama2.clear()
    count = 0
    
    for i in range(900):
        Trama_Float_I.append( tramaI[i] * (1/(2**6)))
        Trama_Float_Q.append( tramaQ[i] * (1/(2**6)))

    print()
    print("TramaI: ", Trama_Float_I)    
    print()
    print()   
    print("TramaQ: ", Trama_Float_Q) 
    print()
    print()

    GuardadoCSV(Trama_Float_I, Trama_Float_Q)

#___Funcion para sub opciones___#
def SubMenu(opc):

    if(opc == '2'):
        
        print("|_____________________parameter options___________________________|")
        print("|( 1 ): Turn on: filter, PRBS, BER, Slizer and counter of Q and I |")
        print("|( 2 ): Trun on: Counter BER Q and I                              |")
        print("|( 3 ): all                                                       |")
        print("|_________________________________________________________________|")
        option = input("Enter an option: ")

        while (option != '1' and option != '2' and option != '3'): 
            option = input("Wrong option. Enter correct option: ")   
        print()
        if (option == '1'): return b'\x01'
        if (option == '2'): return b'\x02'
        if (option == '3'): return b'\x03'

    if(opc == '3'):
        
        print("|__Phase options__|")
        print("|( 1 ): Phase (0) |")
        print("|( 2 ): Phase (1) |")
        print("|( 3 ): Phase (2) |")
        print("|( 4 ): Phase (3) |")
        print("|_________________|")
        option = input("Enter an option: ")

        while (option != '1' and option != '2' and option != '3' and option != '4'): 
            option = input("Wrong option. Enter correct option: ")  
        print()
        if (option == '1'): return b'\x00'
        if (option == '2'): return b'\x01'
        if (option == '3'): return b'\x02'
        if (option == '4'): return b'\x03'

#___main principal del script___#
decode = ''
dispositivo = '01'
while 1 :
    
    print("|__________________MAIN MENU_____________________|")
    print("|( 1 ): Reset globlal                            |")
    print("|( 2 ): Enable filter parameters                 |")
    print("|( 3 ): Phase selection                          |")
    print("|( 4 ): Enable login                             |") #Encenderlo y apagarlo a pata
    print("|( 5 ): Enable read login                        |")
    print("|( 6 ): Bit capture and transmitted errors       |")
    print("|( 7 ): Error or transmitted bits                |")
    print("|( 8 ): Exit the program                         |")
    print("|________________________________________________|")
    entrada = input("Enter an option: ")

    if (entrada == '2' or '3' or '7'):  sub_opc = SubMenu(entrada) #Sub menus para opciones

    if(entrada == '1'): 
        trama = Codificacion (opc_1, b'\x00', dispositivo) 
        Decodificacion(trama)   
    elif(entrada == '2'): 
        trama = Codificacion (opc_2, sub_opc, dispositivo) 
        Decodificacion(trama)
    elif(entrada == '3'): 
        trama = Codificacion (opc_3, sub_opc, dispositivo) 
        Decodificacion(trama)
    elif(entrada == '4'): 
        trama = Codificacion (opc_4, b'\x01', dispositivo) 
        Decodificacion(trama)  
        trama = Codificacion (opc_4, b'\x00', dispositivo) 
        Decodificacion(trama)
    elif(entrada == '5'): 
        trama = Codificacion (opc_5, b'\x01', dispositivo)   
        DecoTramaBitQI(trama)
    elif(entrada == '6'): 
        trama = Codificacion (opc_6, b'\x01', dispositivo)         
        Decodificacion(trama)
    elif(entrada == '7'): 
        trama = Codificacion (opc_7, b'\x00', dispositivo)        
        DecoBitsAndErr(trama)
    elif (entrada  == '8'): ser.close(); break

    else: 
        print("Wrong option. Enter correct option")
        print()
