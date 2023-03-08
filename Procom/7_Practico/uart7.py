#_____________Trabajo Practico N 7 comunicacion puerto serie con la FPGA_________#
#Con el siguien Script se puede enviar comandos a la FPGA para la manipualcion  
#de led's de manera conjunta o individual, asi como pedir el estado de los 
#switch de la misma.
###################################################################################

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

high_byte_amarillo = b'\x0B'
low_byte_amarillo  = b'\x6D'

high_byte_violeta = b'\x06'
low_byte_violeta  = b'\xDB'

high_byte_turquesa = b'\x0D'
low_byte_turquesa  = b'\xB6'

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

#Codificacion para cada opcion de led individual
def bin_leds (opcion):
    if (opcion == "apagado" ): return '000'
    if (opcion == "rojo"    ): return '001'
    if (opcion == "verde"   ): return '100'
    if (opcion == "azul"    ): return '010'
    if (opcion == "amarillo"): return '101'
    if (opcion == "turquesa"): return '110'
    if (opcion == "violeta" ): return '011'
#_______Fin de Codificacion de leds individuales

#Codificacion de envio de trama hacia la FPGA 
def Codificacion(byte_high, byte_low, dispositivo):

    data = byte_high+byte_low

    if (len(data)<=15): #Trama Corta
        cabecera = binascii.unhexlify(str(hex(0xB0+eval(hex(len(data))))).split("0x")[1])
        high = b'\x00'
        low  = b'\x00'
        dispo = binascii.unhexlify(dispositivo)
        cola = binascii.unhexlify(str(hex(0x40+eval(hex(len(data))))).split("0x")[1])
        
        Hex_trama = cabecera + high + low + dispo + data + cola

        trama_list = list(Hex_trama)

    if (len(data)>15):  #Trama Laraga
        data = byte_high+byte_low
        cabecera = b'\xB0'
        cola = b'\x50'
        high = b'\x01'
        low  = b'\xff' 
        dispo = binascii.unhexlify(dispositivo)

        Hex_trama_large = cabecera + high + low + dispo + data + cola

        trama_list = list(Hex_trama_large)
        
    return trama_list
#_______Fin de Codificacion

#____Decodificacion de la Trama enviada por la FPGA Se comprueba si la Trama enviada es la correcta
def Decodificacion (trama):

    dato_1         = ''
    dato_2         = 0
    palabra        = ''
    Error_trama    = 0
    Tamaño_palabra = 0
    cabecera       = bin(trama[0])
    
    if cabecera[2:6] == '1010':
        Pie_trama = bin(trama[len(trama) - 1])
        Tamaño_palabra = int(eval('0b'+ cabecera[6:10]))
        if Tamaño_palabra == 0:
            Error_trama = 1
            print("Error Cabecera")
        else:
            if trama[1] == trama [2] == 0x00:
                Dispositivo = trama[3]
                if (len(trama)-1) == (4 + Tamaño_palabra): 
                    if ('0' + Pie_trama[2:5]) == '0100':
                        if(int(eval('0b'+ Pie_trama[5:9])) == Tamaño_palabra):
                            for k in range (Tamaño_palabra):
                                palabra += chr(trama[k + 4])
                            dato_2 = ord(palabra[1])
                            if (chr(dato_2) == 'F'): Error_trama = 1
                            dato_1 = palabra[0] 
                        else:
                            Error_trama = 1
                            print("Error en tamaño de datos 1") 
                    else:
                        Error_trama = 1
                        print("Error en cola de trama")
                else:
                    Error_trama = 1
                    print("Error en tamaño de datos 2")    
            else:
                Error_trama = 1
                print("Error en los 0x00")
                
    return dato_1, dato_2, Error_trama, Dispositivo
#_______Fin de decodificacion de trama para FPGA  

#_____Deteccion de error: Se toma la trama enviada por la FPGA y se comprueba si es correcta
def deteccion_error (trama):

    ser.write(trama) 
    print("Trama: ", trama)      
    out = []
    time.sleep(2)
    while (ser.inWaiting() > 0):
        readData = ser.read(1) 
        out.append(int.from_bytes(readData,byteorder='big'))

    if (len(out) != 0):
        dato1, dato2, flagError, Dispositivo = Decodificacion(out)
        # print("Trama enviada por la FPGA: ",out)
        # print("Valor de Flag: "   ,flagError)
        # print("Valor de dato1: "  ,dato1)     #Descomentar para testeo
        # print("Valor de dato2: "  ,dato2)
        # print("Valor de Dispo: "  ,Dispositivo)
        if (flagError == 1):
            print("Error Encontrado",chr(dato2)) #Si hay un error lsa FPGA eniva una F
        else:
            print("Valor de los Switch: ",dato2) #Si no hya error la FPGA envia el valor de los switch

        print("") 
        out.clear()     
        time.sleep(1)
#_______Fin de deteccion de error

# main()
dispositivo = '01'
while 1 :
    
    print("\n|_________________________________________________________________|")
    print("|____________________PUERTO SERIE para FPGA_______________________|")
    print("|Ingrese una de las siguientes opciones                           |")
    print("|OPCION (led     ): Configurar los leds                           |")
    print("|OPCION (estado  ): Devuelve el estado de salida de los switch's  |")
    print("|OPCION (exit    ): Finaliza el programa                          |")
    print("|_________________________________________________________________|\n")
    inputData = input("Opcion: ")
    





    
    if (inputData == 'exit'):
        ser.close()
        break

    elif (inputData == 'estado'):  
            trama = Codificacion(high_byte_state,low_byte_state, dispositivo)
            deteccion_error(trama)
           
    elif (inputData == 'led'):
            print("\n|_________________________________________________________________|")
            print("|___________________________CONTROL_______________________________|")
            print("|OPCION (all       ): Controla todos los leds                     |")
            print("|OPCION (individual): Controla los leds de forma individual       |")
            print("|_________________________________________________________________|\n")
            inputData = input("Opcion: ")
            
            while (inputData != 'all' and inputData != 'individual'):
                inputData = input("Opcion incorrecta. Ingrese Nuevamente: ")
            
            if (inputData == 'all'):
                print("\n|_________________________________________________________________|")
                print("|____________________CONFIGURACION DE LEDS________________________|")
                print("|OPCION (apagado ): Apaga el led                                  |")
                print("|OPCION (rojo    ): Prende los led de color Rojo                  |")
                print("|OPCION (azul    ): Prende los led de color azul                  |")
                print("|OPCION (verde   ): Prende los led de color verde                 |")
                print("|OPCION (amarillo): Prende los led de color amarillo              |")
                print("|OPCION (turquesa): Prende los led de color turquesa              |")
                print("|OPCION (violeta ): Prende los led de color violeta               |")
                print("|_________________________________________________________________|\n")
                inputData = input("Opcion: ")
                while (inputData != 'apagado' and inputData != 'rojo' and inputData != 'azul' and inputData != 'verde' 
                       and inputData != 'amarillo' and inputData != 'turquesa' and inputData != 'violeta'):
                    
                    inputData = input("Opcion incorrecta. Ingrese Nuevamente: ")
                
                if (inputData == 'rojo'  ): 
                    trama = Codificacion(high_byte_red,low_byte_red, dispositivo) 
                    print(trama)

                if (inputData == 'azul'  ): 
                    trama = Codificacion(high_byte_blue,low_byte_blue, dispositivo)
                    print(trama)

                if (inputData == 'verde' ): 
                    trama = Codificacion(high_byte_green,low_byte_green, dispositivo)
                    print(trama)

                if (inputData == 'amarillo' ): 
                    trama = Codificacion(high_byte_amarillo,low_byte_amarillo, dispositivo)
                    print(trama)

                if (inputData == 'turquesa' ): 
                    trama = Codificacion(high_byte_turquesa,low_byte_turquesa, dispositivo)
                    print(trama)

                if (inputData == 'violeta' ): 
                    trama = Codificacion(high_byte_violeta,low_byte_violeta, dispositivo)
                    print(trama)

                if (inputData == 'apagado' ): 
                    trama = Codificacion(b'\x00',b'\x00', dispositivo)
                    print(trama)
                deteccion_error(trama)
            elif (inputData == 'individual'):
                print("|_________________________________________________________________|")
                print("|____________________CONFIGURACION DE LEDS________________________|")
                print("|OPCION (apagado ): Apaga el led                                  |")
                print("|OPCION (rojo    ): Prende el led de color Rojo                   |")
                print("|OPCION (azul    ): Prende el led de color azul                   |")
                print("|OPCION (verde   ): Prende el led de color verde                  |")
                print("|OPCION (amarillo): Prende el led de color amarillo               |")
                print("|OPCION (turquesa): Prende el led de color turquesa               |")
                print("|OPCION (violeta ): Prende el led de color violeta                |")
                print("|_________________________________________________________________|\n")
                inputData3 = input("LED 3: ")
                inputData2 = input("LED 2: ")
                inputData1 = input("LED 1: ")
                inputData0 = input("LED 0: ")
                while (inputData3 != 'apagado' and inputData3 != 'rojo' and inputData3 != 'azul' and inputData3 != 'verde' 
                       and inputData3 != 'amarillo' and inputData3 != 'turquesa' and inputData3 != 'violeta'): 
                    
                    inputData3 = input("Opcion incorrecta. Ingrese nuevamente LED 3: ")
                    
                while (inputData2 != 'apagado' and inputData2 != 'rojo' and inputData2 != 'azul' and inputData2 != 'verde' 
                       and inputData2 != 'amarillo' and inputData2 != 'turquesa' and inputData2 != 'violeta'): 
                    
                    inputData2 = input("Opcion incorrecta. Ingrese nuevamente LED 2: ")
                    
                while (inputData1 != 'apagado' and inputData1 != 'rojo' and inputData1 != 'azul' and inputData1 != 'verde' 
                       and inputData1 != 'amarillo' and inputData1 != 'turquesa' and inputData1 != 'violeta'): 
                    
                    inputData1 = input("Opcion incorrecta. Ingrese nuevamente LED 1: ")
                    
                while (inputData0 != 'apagado' and inputData0 != 'rojo' and inputData0 != 'azul' and inputData0 != 'verde' 
                       and inputData0 != 'amarillo' and inputData0 != 'turquesa' and inputData0 != 'violeta'): 
                    
                    inputData0 = input("Opcion incorrecta. Ingrese nuevamente LED 0: ")
                    
                codigo = '0000' + bin_leds(inputData3) + bin_leds(inputData2) + bin_leds(inputData1) + bin_leds(inputData0)
                codigo_high = hex(eval('0b' + codigo[0:8]))
                codigo_low  = hex(eval('0b' + codigo[8:17]))
                if (len(codigo_high) == 3):
                    codigo_high = codigo_high[0:2] + '0' + codigo_high[2]

                if (len(codigo_low) == 3):
                    codigo_low = codigo_low[0:2] + '0' + codigo_low[2]
                
                codigo_high = binascii.unhexlify(codigo_high.split("0x")[1])
                codigo_low = binascii.unhexlify(codigo_low.split("0x")[1])
                
                trama = Codificacion(codigo_high,codigo_low, dispositivo)
                print(trama)
                deteccion_error(trama)
                
