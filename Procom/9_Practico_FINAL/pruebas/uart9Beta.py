####################################################################################
#   Autor: Juarez Daniel, Jose Gomez Lazarte
#   Año: 2023
#   Nombre: uart9.py 1.0b para comunicacion entre FPGA y la PC en el proyecto integrador
#   Descripcion: 
#               Se trato de poder guardar no solo la salida de los filtros sino tambien               
#   poder detectar con que offset fue guardado los datos y en base a eso obtener la         
#   contelacion rotada o sin rotar. Se logro sin rotar pero para datos debido a una 
#   rotacion no se logro conseguir el offset debido a latencias propias en la FPGA
#   se espera en un futuro poder mejorarlo para que quede de manera automatica.
###################################################################################

import time
import serial
import sys
import binascii 
import csv
import numpy    as np

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

#___Funcion para guardado de los datos de la constelacion recolectados de los filtros___#
def GuardadoConstelacionCSV(trama_constelacion_I, trama_constelacion_Q, tipo_de_dato):

    if (tipo_de_dato == 'FALSE'):
        archivo = open('DatosConstelacionI.csv', '+w') #con +w si no existe el archivo se lo crea
    else:
        archivo = open('DatosConstelacionRotadaI.csv', '+w') #con +w si no existe el archivo se lo crea       

    for i in range(len(trama_constelacion_I)):
        archivo.write(str(trama_constelacion_I[i]))
        archivo.write(',')

    if (tipo_de_dato == 'FALSE'):        
        print("Writing complete DatosConstelacionI")
    else:
        print("Writing complete DatosConstelacionRotadaI")           
    archivo.close()


    if (tipo_de_dato == 'FALSE'):
        archivo = open('DatosConstelacionQ.csv', '+w') #con +w si no existe el archivo se lo crea
    else:
        archivo = open('DatosConstelacionRotadaQ.csv', '+w') #con +w si no existe el archivo se lo crea 
    for i in range(len(trama_constelacion_Q)):
        archivo.write(str(trama_constelacion_Q[i]))
        archivo.write(',')

    if (tipo_de_dato == 'FALSE'):        
        print("Writing complete DatosConstelacionQ")
    else:
        print("Writing complete DatosConstelacionRotadaQ") 
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
def Codificacion(opc, sub_opc , rell_opc, dispositivo) :

    data = opc + enable + rell_opc + sub_opc    #for example: 0x03 + 0x80 + 0x00 + 0x01 = 0x203800001
    # print(data)

    if (len(data)<=15):
        cabecera = binascii.unhexlify(str(hex(0xA0+eval(hex(len(data))))).split("0x")[1])
        high = b'\x00'
        low  = b'\x00'
        dispo = binascii.unhexlify(dispositivo)
        cola = binascii.unhexlify(str(hex(0x40+eval(hex(len(data))))).split("0x")[1])
        
        Hex_trama = cabecera + high + low + dispo + data + cola

        print("Trama: ", Hex_trama)
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
def DecoTramaBitQI(trama, sub_opc):

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
        Trama_Float_I.append( tramaI[i] * (1/(2**6)))   #Se cuantiza los datos para amplitud +/- 1,5
        Trama_Float_Q.append( tramaQ[i] * (1/(2**6)))   #REVISAR 

    print()
    print("TramaI: ", Trama_Float_I)    
    print()
    print()   
    print("TramaQ: ", Trama_Float_Q) 
    print()
    print()

    if (sub_opc == '1'):
        GuardadoCSV(Trama_Float_I, Trama_Float_Q)   #Se guardan los datos de los filtros en crudo

    elif(sub_opc == '2'):   #Se bsuca obtener la constelacion en base a los datos recibidios 

        #_______________________________Variables_____________________________________________#
        posicion_partida_Q = -1
        posicion_partida_I = -1
        Trama_Constelation_Q      =   []        #Donde se almacenan las constelaciones
        Trama_Constelation_I      =   [] 
        lista_Cos = []                          # Para ondas de referencia
        lista_Sin = []
        N            = 1024                     # Muestras
        Os           = 4.0                      # Oversampling    
        frec         = 1.0/((1.0/100.0e6)*N)    # Frecuencia
        valorI       = 0                        # Valores para calculos sobre datos rotados
        valorQ       = 0            
        dato = int(input("Ingrese la Frecuencia que fue elejida anteriormente: "))

        DENOMINADOR = (N//(2**(dato-1)))
        PASO = N//DENOMINADOR                     # Cantidad de pasos dados
        flag = 'FALSE'
        #_______________________________________________________________________________________#


        #_____En caso de que la constelacion no posee una rotacion_____#                                        
        for i in range (len(Trama_Float_Q)):    #Se busca una posicion de partida debido a que los datos recibidos no estan desde la posicion 0
            if ((Trama_Float_Q[i] >= 0.99 and Trama_Float_Q[i] <= 1.005) or (Trama_Float_Q[i] <= -0.99 and Trama_Float_Q[i] >= -1.005)): posicion_partida_Q = i
            if ((Trama_Float_I[i] >= 0.99 and Trama_Float_I[i] <= 1.005) or (Trama_Float_I[i] <= -0.99 and Trama_Float_I[i] >= -1.005)): posicion_partida_I = i        
            if(posicion_partida_Q != -1 and posicion_partida_I != -1 ): 
                flag =='TRUE'
                break
        #Descomentar para testeo            
        print("Punto de partida Q: ", posicion_partida_Q)   
        print("Punto de partida I: ", posicion_partida_I)
        print()

        n = posicion_partida_Q  
        m = posicion_partida_I   

        if (flag == 'FALSE'):                       #A partir de ese punto de partida se realizan pasos de acuerdo al Oversampling (Os)
           for i in range (len(Trama_Float_Q)):     #Usado    

                if (Trama_Float_Q[n] == -1.0 or Trama_Float_Q[n] == 1.0):   #Se detecta si los valores recibidos tuvieron una rotacion
                    Trama_Constelation_Q.append(Trama_Float_Q[n])
                if (Trama_Float_I[m] == -1.0 or Trama_Float_I[m] == 1.0):
                    Trama_Constelation_I.append(Trama_Float_I[n])
                                                                            #En caso de que el patron de datos de 1 y -1             
                elif(Trama_Float_Q[n] != -1.0 or Trama_Float_Q[n] != 1.0 or Trama_Float_I[m] != -1.0 or Trama_Float_I[m] != 1.0):
                    print("Constelacion esta Rotada")
                    print()
                    Trama_Constelation_Q.clear()
                    Trama_Constelation_I.clear()
                    flag = 'TRUE'
                    break
                if(((n + 4)) < len(Trama_Float_Q)):
                    n = (n + 4) 
                else: break 
                if(((m + 4)) < len(Trama_Float_I)):
                    m = (m + 4) 
                else: break   

        #_____En caso de que la constelacion posee una rotacion_____#
        if(flag == 'TRUE'):   
            posicion_partida_Q = 0
            posicion_partida_I = 0

            for t in range(4096):                               #Se genera una onda Sen y Cos de referencia
                valor = np.sin((np.pi/2.0)*frec*(t/100.0e6))
                lista_Sin.append(valor)

            for t in range(4096):
                valor = np.cos((np.pi/2.0)*frec*(t/100.0e6))
                lista_Cos.append(valor)

            lista_Sin = list(lista_Sin)
            lista_Cos = list(lista_Cos)

            n = 0  
                                                                #En caso de tener una rotacion se bsuca el punto de partida
            for t in range(4):                                  #para almacenar los datos relacionados con los -1 y 1 antes de la operatoria

                valorQ = (Trama_Float_I[t] - ((lista_Sin[n] / lista_Cos[n])*Trama_Float_Q[t])) / (((lista_Sin[n]**2) / lista_Cos[n]) + lista_Cos[n])
                valorI = (Trama_Float_Q[t] + (valorQ * lista_Sin[n])) / (lista_Cos[n])
                
                print('PASO:', n)                                                                                        #era un 1 o un -1                
                if  ((PASO-1) == 0): n = n + PASO              
                if  ((PASO-1) != 0): n = n + (PASO-1)

                print("Valor Q",valorQ)
                print()                     
                print("Valor I",valorI)
                print()
                if ((valorQ >= 0.99 and valorQ <= 1.005) or (valorQ <= -0.99 and valorQ >= -1.005)):        #CREO QUE HAY QEU DAR MAS RANGO
                    posicion_partida_Q = t
                    print("valor de posicion Q: ", posicion_partida_Q)
                    if ((valorI >= 0.99 and valorI <= 1.005) or (valorI <= -0.99 and valorI >= -1.005)):
                        posicion_partida_I = t
                        print("valor de posicion I: ", posicion_partida_I) 
                        if (posicion_partida_I != -1 and posicion_partida_Q != -1): break        

            #Descomentar para testear
            print("posicion optimaQ: ", posicion_partida_Q)         
            print("posicion optimaI: ", posicion_partida_I)

            Trama_Constelation_I = Trama_Float_I [posicion_partida_I:len(Trama_Float_I):int(Os)]    #Cuando se econtro un -1 o un 1 a partir de esa posicion 
            Trama_Constelation_Q = Trama_Float_Q [posicion_partida_Q:len(Trama_Float_Q):int(Os)]    #se guardan los datos correctos cada x muestras segun el Os   
            print("largoI: ", len(Trama_Constelation_I))    
            print("largoQ: ", len(Trama_Constelation_Q))     


        GuardadoConstelacionCSV(Trama_Constelation_I, Trama_Constelation_Q, flag)               #Pasamos los datos de la constelacion para ser almacenados 

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
        if (option == '1'): return b'\x01', b'\x00'
        if (option == '2'): return b'\x02', b'\x00'
        if (option == '3'): return b'\x03', b'\x00'

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
        if (option == '1'): return b'\x00', b'\x00'
        if (option == '2'): return b'\x01', b'\x00'
        if (option == '3'): return b'\x02', b'\x00'
        if (option == '4'): return b'\x03', b'\x00'

    if(opc == '4'):
        optionFrec  =   ''    
        print("|____________Login options____________|")
        print("|( 1 ): Login output Filters          |")
        print("|( 2 ): Login output Err Quadr Filter |")
        print("|_____________________________________|")
        option = input("Enter an option: ")

        while (option != '1' and option != '2'): 
            option = input("Wrong option. Enter correct option: ")  

        if( option == '2'):
            
            print("|____Selec Freq the rotation____|")
            print("|( 1 ):  Frequency: 24.414  kHz |") #dato: 0X00
            print("|( 2 ):  Frequency: 48.828  kHz |") #dato: 0X01
            print("|( 3 ):  Frequency: 97.656  kHz |") #dato: 0X02
            print("|( 4 ):  Frequency: 195.31  kHz |") #dato: 0X03
            print("|( 5 ):  Frequency: 390.62  kHz |") #dato: 0X04
            print("|( 6 ):  Frequency: 781.25  kHz |") #dato: 0X05
            print("|( 7 ):  Frequency: 1.5626  MHz |") #dato: 0X06
            print("|( 8 ):  Frequency: 3.1250  MHz |") #dato: 0X07
            print("|( 9 ):  Frequency: 6.250   MHz |") #dato: 0X08
            print("|( 10 ): Frequency: 12.500  MHz |") #dato: 0X09 
            print("|( 11 ): Frequency: 25.000  MHz |") #dato: 0X0A                                                                      
            print("|_______________________________|")
            optionFrec = input("Selec frequency: ")

            while ( optionFrec != '1'  and optionFrec != '2' and optionFrec != '3' and optionFrec != '4' 
                and optionFrec != '5' and optionFrec != '6' and optionFrec != '7'  and optionFrec != '8' 
                and optionFrec != '9' and optionFrec != '10' and optionFrec != '11' ): 
                optionFrec = input("Wrong option. Enter correct option: ")  

        print()
        if (option == '1'): return b'\x01', b'\x00' 
        if (option == '2' and optionFrec == '1' ):  return b'\x03', b'\x00'
        if (option == '2' and optionFrec == '2' ):  return b'\x03', b'\x01'
        if (option == '2' and optionFrec == '3' ):  return b'\x03', b'\x02'
        if (option == '2' and optionFrec == '4' ):  return b'\x03', b'\x03'
        if (option == '2' and optionFrec == '5' ):  return b'\x03', b'\x04'
        if (option == '2' and optionFrec == '6' ):  return b'\x03', b'\x05'
        if (option == '2' and optionFrec == '7' ):  return b'\x03', b'\x06'
        if (option == '2' and optionFrec == '8' ):  return b'\x03', b'\x07'
        if (option == '2' and optionFrec == '9' ):  return b'\x03', b'\x08'
        if (option == '2' and optionFrec == '10' ): return b'\x03', b'\x09'
        if (option == '2' and optionFrec == '11' ): return b'\x03', b'\x0A'

    if(opc == '5'):
        print("|_____________Selec Data____________|")
        print("|( 1 ): Salve data output filter    |")
        print("|( 2 ): Salve data the constelation |")
        print("|___________________________________|")
        optionData = input("Selec Salve: ")
        while (optionData != '1' and optionData != '2'):                                                 
            optionData = input("Wrong option. Enter correct option: ")
    
        return optionData, b'\x00'


#___main principal del script___#
decode = ''
dispositivo = '01'
while 1 :
    
    print("|__________________MAIN MENU_____________________|")
    print("|( 1 ): Reset globlal                            |")
    print("|( 2 ): Enable filter parameters                 |")
    print("|( 3 ): Phase selection                          |")
    print("|( 4 ): Enable login                             |") 
    print("|( 5 ): Enable read login                        |")
    print("|( 6 ): Bit capture and transmitted errors       |")
    print("|( 7 ): Error or transmitted bits                |")
    print("|( 8 ): Exit the program                         |")
    print("|________________________________________________|")
    entrada = input("Enter an option: ")

    # if (entrada == '2' or '3' or '4' or '5'):   
    #     sub_opc, rell_opc = SubMenu(entrada) #Sub menus para opciones

    if(entrada == '1'): 
        trama = Codificacion (opc_1, b'\x00', b'\x00', dispositivo)  
        Decodificacion(trama)   

    elif(entrada == '2'): 
        sub_opc, rell_opc = SubMenu(entrada) #Sub menus para opciones       
        trama = Codificacion (opc_2, sub_opc, rell_opc, dispositivo)  
        Decodificacion(trama)

    elif(entrada == '3'): 
        sub_opc, rell_opc = SubMenu(entrada) #Sub menus para opciones        
        trama = Codificacion (opc_3, sub_opc, rell_opc, dispositivo)  
        Decodificacion(trama)

    elif(entrada == '4'): 
        sub_opc, rell_opc = SubMenu(entrada) #Sub menus para opciones  

        trama = Codificacion (opc_4, b'\x00', rell_opc, dispositivo)  #Set pasos  
        Decodificacion(trama)               

        trama = Codificacion (opc_1, b'\x00', b'\x00', dispositivo)  #Reset
        Decodificacion(trama) 

        trama = Codificacion (opc_4, sub_opc, rell_opc, dispositivo)  #logueo
        Decodificacion(trama)  

        trama = Codificacion (opc_4, b'\x00', rell_opc, dispositivo)  #fin de logueo
        Decodificacion(trama)

    elif(entrada == '5'): 
        sub_opc, rell_opc = SubMenu(entrada) #Sub menus para opciones        
        trama = Codificacion (opc_5, b'\x01', b'\x00', dispositivo)  #TESTEAR EN FPGA   
        DecoTramaBitQI(trama,sub_opc)

    elif(entrada == '6'): 
        trama = Codificacion (opc_6, b'\x01', b'\x00', dispositivo)          
        Decodificacion(trama)
    elif(entrada == '7'): 
        trama = Codificacion (opc_7, b'\x00', b'\x00', dispositivo)         
        DecoBitsAndErr(trama)
    elif (entrada  == '8'): ser.close(); break

    else: 
        print("Wrong option. Enter correct option")
        print()



    #FALTA AGREGAR OPC DE CONSTELACION NORMAL Y CON ERROR
