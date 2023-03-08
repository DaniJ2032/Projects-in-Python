#____________MANEJO DE PUERTO SERIE EN PYTHON______________

import TP1_menu as tp1 # importamos TP1
import TP2_menu as tp2 # importamos TP2
import binascii
import serial          # Manejo de puerto serie

ser = serial.serial_for_url('loop://', timeout=1)

ser.isOpen()
ser.timeout=None
ser.flushInput()
ser.flushOutput()

#Codificacion
def Codificacion(entrada, dispositivo):

    dato = entrada.encode()

    if (len(entrada) <= 15):
        cabecera = binascii.unhexlify(str(hex(0xA0+eval(hex(len(dato))))).split("0x")[1])
        high = b'\x00'
        low  = b'\x00'
        dispo = binascii.unhexlify(dispositivo)
        cola = binascii.unhexlify(str(hex(0x40+eval(hex(len(dato))))).split("0x")[1])
        
        Hex_trama = cabecera + high + low + dispo + dato + cola
        #print("Trama en Hex: ", Hex_trama)
        trama_list = list(Hex_trama)

    if (len(entrada) > 15):

        cabecera = b'\xB0'
        cola = b'\x50'
        high = b'\x01'
        low  = b'\xff' 
        dispo = binascii.unhexlify(dispositivo)

        Hex_trama_large = cabecera + high + low + dispo + dato + cola
        #print("Trama larga en Hex: ", Hex_trama_large)
        trama_list = list(Hex_trama_large)
        
    return trama_list 
#___________________Fin de Codificacion

#Decodificacion
def Decodificacion(trama):

    #CODIFICANDO EL MENSAJE
    trama = ser.write(trama) # Codificando mensaje en el puerto serie

    large = ser.inWaiting()
    cabecera = 4
    read_data = []
    opc = ''

    while (ser.inWaiting() > 0):  
        read_data.append(chr(ord(ser.read(1)))) #recojo los datos de a 1byte

    opc = "".join(read_data[cabecera:large-1]) #detecto el mensaje
    
    return opc  
#___________________Fin de Decodificacion


#main()
print("|_________________________________________________|")
print("|_____________PUERTO SERIA V1.0_PuntoC____________|")
print("|Ingrese una de las siguientes opciones           |")
print("|OPCION calculadora: Scrip de Calculadora         |")
print("|OPCION graficadora: Scrip de Graficadora         |")
print("|OPCION exit: salir del programa                  |")
print("|_________________________________________________|")
print()
flag1=0
dispositivo = '01'  #numero de dispositivo

while 1 :

    if flag1 == 0:
        data = input("Opcion: ")
    if (data == "exit"):
        if ser.isOpen():
            ser.close()
            break


    trama = Codificacion(data, dispositivo)    #codificando la trama
    
    decode = Decodificacion(trama)             #decodifico la trama

    if (decode == 'calculadora'): tp1.Menu() 
    if (decode == 'graficadora'): tp2.menu()
    print()

    while (decode != "calculadora" and decode != "graficadora"):
        print("Se ingreso alguna opcion mal, reintentelo nuevamente")

        data = input("Opcion: ")

        trama = Codificacion(data, dispositivo)    #codificando la trama
        decode = Decodificacion(trama)             #decodifico la trama
        flag1=1

        if(flag1==1):
            if (decode=="calculadora"): 
                tp1.Menu() 
                flag1=0
            if (decode=="graficadora"): 
                tp2.menu()
                flag1=0
            print()
            break
# fin de main
