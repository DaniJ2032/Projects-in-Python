#____________MANEJO DE PUERTO SERIE EN PYTHON______________
import TP1_menu as tp1 # importamos TP1
import TP2_menu as tp2 # importamos TP2
# import time            # manejo de tiempos
import serial          # manejo de puerto serie  

ser = serial.serial_for_url('loop://', timeout=1)

ser.isOpen()
ser.timeout=None
ser.flushInput()
ser.flushOutput()
print("|_________________________________________________|")
print("|_____________PUERTO SERIA V1.0_PuntoA____________|")
print("|Ingrese una de las siguientes opciones           |")
print("|OPCION 1: Scrip de Calculadora                   |")
print("|OPCION 2: Scrip de Graficadora                   |")
print("|OPCION 3: escriba exit para salir                |")
print("|_________________________________________________|")
print()

flag1=0

while 1 :
    if flag1 == 0:
        data = input("Opcion: ")

    if (data == 'exit'):
        if ser.isOpen():
            ser.close()
            break

    if data !=0 :
        ser.write(data.encode()) #codifico el dato de entrada y escribo en el puerto
        opc = ''  
        while ser.inWaiting() > 0:
            read_data = ser.read(1)
            opc += read_data.decode()
            if opc != '': flag1=0

        if (opc=="1"): tp1.Menu() # abrimos el TP1
        if (opc=="2"): tp2.menu() # abrimos el TP2
        print()

        while ( opc != "1" and opc != "2" ):
            print("Se ingreso alguna opcion mal, reintentelo nuevamente")
            data = input("Opcion: ")
            ser.write(data.encode())
            read_data = ser.read(1)
            flag1 = 1
            break


















