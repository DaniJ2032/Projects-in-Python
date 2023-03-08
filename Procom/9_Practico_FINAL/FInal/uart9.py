####################################################################################
#   Autor: Juarez Daniel, Jose Gomez Lazarte
#   Año: 2023
#   Nombre: uart9.py para comunicacion entre FPGA y la PC en el proyecto integrador
#   Descripcion: 
#               Mediante este scripts se se comunica la PC con la FPGA de esta manera          
#               se puede resetear, setear y pedir datos a la FPGA y almacenarlos en 
#               archivos .csv para posteriormente poder ser graficados ya sea en python    
#               u otro soft.    
###################################################################################

#___Librerias
import time
import serial
import sys
import binascii 
import numpy    as np

#___Comunicacion puerto Serie para la FPGA
portUSB = sys.argv[1]
ser = serial.Serial(
   port='/dev/ttyUSB{}'.format(int(portUSB)),	# Seteo del puerto
   baudrate=115200,
   parity=serial.PARITY_NONE,
   stopbits=serial.STOPBITS_ONE,
   bytesize=serial.EIGHTBITS
)
ser.isOpen()
ser.timeout=None
print(ser.timeout)
################################

#___Code 
enable = b'\x80'
opc_1  = b'\x00' 
opc_2  = b'\x01'
opc_3  = b'\x02'
opc_4  = b'\x03'
opc_5  = b'\x04'
opc_6  = b'\x05'
opc_7  = b'\x06'
##############################################

#|___Funcion para guardado de los datos recolectados de las salidas del filtro___|
#| RECIBE:                                                                       |   
#|       tramaI  y tramaQ = Datos obtenidos de la lectura de la RAM              |
#|       sub_opc_read_log = Dependiendo de su valor sera el nombre con que       |
#|       se almacena los datos                                                   |
#| RETORNA:                                                                      |
#|         Nada                                                                  |
#|_______________________________________________________________________________|
def GuardadoCSV(tramaI, tramaQ, sub_opc_read_log):

    if( sub_opc_read_log == '1'): # Dependiendo del valor de la sub opcion es el nombre del archivo a crear
        archivo = open('DatosFiltroI.csv', '+w') #con +w si no existe el archivo se lo crea
    else:
        archivo = open('DatosFiltroRotadoI.csv', '+w')   
    for i in range(len(tramaI)):
        archivo.write(str(tramaI[i]))   # Almacenamiento de los datos obtenidos
        archivo.write(',')
    
    if( sub_opc_read_log == '1'):    
        print("Writing complete DatosFiltroI")
    else:
        print("Writing complete DatosFiltroRotadoI")
    archivo.close()

    if( sub_opc_read_log == '1'):
        archivo = open('DatosFiltroQ.csv', '+w') #con +w si no existe el archivo se lo crea
    else:
        archivo = open('DatosFiltroRotadoQ.csv', '+w')  
    for i in range(len(tramaQ)):
        archivo.write(str(tramaQ[i]))
        archivo.write(',')
    if( sub_opc_read_log == '1'):    
        print("Writing complete DatosFiltroQ")
    else:
        print("Writing complete DatosFiltroRotadoQ")
    print()
    print()
    archivo.close()

#|_____Funcion para corroborar las tramas de los bits y errores transmitidos asi como la de los filtros_____|
#| RECIBE:                                                                                                  |   
#|       TramaOK = Una trama completa enviada por la fpga al python, puede ser del filtro, de bits o de err |
#| RETORNA:                                                                                                 |
#|         Var OK = 1 trama correcta, OK = O Error en trama recibida                                        |
#|________________________________________________________________________________________________________  |
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

#|_______________Funcion para armar la trama a enviar a la FPGA____________________|
#| RECIBE:                                                                         |   
#|        opc = Var que indica la operacion a realizar en el RF de la fpga         |
#|        sub_opc = var de sub opcion para op. especificas en la fpga              |
#|        rell_opc = var que puede ser 0  o un valor especifico en ciertas opc     |
#|        dispositivo = Var que indica el num de dispositivo con el que se trabaja |
#| RETORNA:                                                                        |
#|        trama_list = Devuelve la trama armada para ser escrita en el puerto uart |
#|_________________________________________________________________________________|
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

#|____Funcion para decodificar algun error en el envio de tramas hacia la FPGA___|
#| RECIBE:                                                                       |   
#|         trama =  la trama armada para ser enviada por el puerto y tambien     |
#|         esta a la espera si al micro de la fpga envia un mensaje de error     |
#| RETORNA:                                                                      |
#|         Nada                                                                  |
#|_______________________________________________________________________________|
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
#| RECIBE:                                                                       |   
#|       tramaI  y tramaQ = Datos obtenidos de la lectura de la RAM              |
#|       sub_opc_read_log = Dependiendo de su valor sera el nombre con que       |
#|       se almacena los datos                                                   |
#| RETORNA:                                                                      |
#|         Nada                                                                  |
#|_______________________________________________________________________________|   
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

#|____________Funcion para decodificar los datos de los filtros__________________ |
#| RECIBE:                                                                        |   
#|        trama = trama que fue enviada para la lectura de los datos guardados en |
#|        la RAM, a su vez se decodifica los datos que envia la FPGA por trama    |
#|        y se obtienen los valores a las salidas del filtro.                     |
#|        sub_opc_read_log = var auxiliar que se la pasa a otra funcion encargada |
#|        de guardar los datos enviados al python.                                |
#| RETORNA:                                                                       |
#|         Nada                                                                   |
#|________________________________________________________________________________|
def DecoTramaBitQI(trama, sub_opc_read_log):

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

    # print()
    # print("TramaI: ", Trama_Float_I)    
    # print()
    # print()   
    # print("TramaQ: ", Trama_Float_Q) 
    # print()
    # print()

    GuardadoCSV(Trama_Float_I, Trama_Float_Q, sub_opc_read_log)   #Se guardan los datos de los filtros en crudo

#|_____________________Funcion para sub opciones_______________________|
#| RECIBE:                                                             |
#|        opc = Var que indica la opcion escojia, algunas opciones     |
#|        cuentan con un sub menu para sub opciones como por ejemplo   |
#|        la opcion de seteo de partes del sistema                     |
#| RETORNA:                                                            |
#|         sub_opc = var que indica una sub opcion dependiendo de la   |
#|         opcion principal                                            |
#|         rell_opc = retorna un valor ya sea cero o uno en especifico |
#|         segun la opcion y sub_opc elegida                           |
#|_____________________________________________________________________|
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


#|___________________main principal del script___________________________|
#| Desde aca se parte del menu principal donde se escje la opcion que se |
#| desea realizar.                                                       |
#|_______________________________________________________________________|
#___Variables___#
dispositivo      = '01' # N de dispositivo utilizado
sub_opc          = ''   # var de sub opcion solo para algunas opciones
sub_opc_read_log = ''   # Var aux solo para guardado de datos logeados  
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

    if(entrada == '1'):                                                # Reset para el sistema                                         
        trama = Codificacion (opc_1, b'\x00', b'\x00', dispositivo)  
        Decodificacion(trama)   

    elif(entrada == '2'):                                              # Seteo de las diferentes partes del sistema
        sub_opc, rell_opc = SubMenu(entrada) #Sub menus para opciones       
        trama = Codificacion (opc_2, sub_opc, rell_opc, dispositivo)  
        Decodificacion(trama)

    elif(entrada == '3'):                                             # Seleccion de la fase, por defecto es la cero
        sub_opc, rell_opc = SubMenu(entrada)         
        trama = Codificacion (opc_3, sub_opc, rell_opc, dispositivo)  
        Decodificacion(trama)

    elif(entrada == '4'):                                             # Logeo de datos del filtro en la RAM  
        sub_opc, rell_opc = SubMenu(entrada)  

        trama = Codificacion (opc_4, b'\x00', rell_opc, dispositivo) #Set pasos  
        Decodificacion(trama)               

        trama = Codificacion (opc_1, b'\x00', b'\x00', dispositivo) #Reset
        Decodificacion(trama) 

        trama = Codificacion (opc_4, sub_opc, rell_opc, dispositivo) #logueo
        Decodificacion(trama)  

        trama = Codificacion (opc_4, b'\x00', rell_opc, dispositivo) #fin de logueo
        Decodificacion(trama)
        if (sub_opc == b'\x01'): sub_opc_read_log = '1'
        else: sub_opc_read_log = '0'

    elif(entrada == '5'):                                            # Lectura de los datos logeados       
        trama = Codificacion (opc_5, b'\x01', b'\x00', dispositivo)     
        DecoTramaBitQI(trama,sub_opc_read_log)

    elif(entrada == '6'):                                            # Captura de bits y errores transmitidos           
        trama = Codificacion (opc_6, b'\x01', b'\x00', dispositivo)          
        Decodificacion(trama)
    elif(entrada == '7'):                                            # Lectura de los bits y errores transmitidos
        trama = Codificacion (opc_7, b'\x00', b'\x00', dispositivo)         
        DecoBitsAndErr(trama)
    elif (entrada  == '8'): ser.close(); break                       # Fin de programa

    else: 
        print("Wrong option. Enter correct option")
        print()

