#____________MANEJO DE PUERTO SERIE EN PYTHON______________
import TP1_menu as tp1 # importamos TP1
import TP2_menu as tp2 # importamos TP2
import serial          # manejo de puerto serie  

ser = serial.serial_for_url('loop://', timeout=1)

ser.isOpen()
ser.timeout=None
ser.flushInput()
ser.flushOutput()
print("|_________________________________________________|")
print("|_____________PUERTO SERIA V1.0_PuntoB____________|")
print("|Ingrese una de las siguientes opciones           |")
print("|OPCION calculadora: Scrip de Calculadora         |")
print("|OPCION graficadora: Scrip de Graficadora         |")
print("|OPCION exit: salir del programa                  |")
print("|_________________________________________________|")
print()
flag1=0

while 1 :

    if flag1 == 0:
        data = input("Opcion: ")
    if (data == "exit"):
        if ser.isOpen():
            ser.close()
            break

    ser.write(data.encode()) #codifico el dato de entrada y escribo en el puerto
    opc = ''  

    while ser.inWaiting() > 0:
        read_data = ser.read(1)     #leemos de a 1byte (1 carcter) a la vez
        opc += read_data.decode()   #leo lo tomado del puerto y lo concateno en una salida

    if (opc == 'calculadora'): tp1.Menu() 
    if (opc == 'graficadora'): tp2.menu()
    print()

    while (opc != "calculadora" and opc != "graficadora"):
        print("Se ingreso alguna opcion mal, reintentelo nuevamente")
        opc = ''
        data = input("Opcion: ")
        ser.write(data.encode())

        while ser.inWaiting() > 0:

            read_data = ser.read(1)
            opc += read_data.decode()
            if opc != '': flag1=1
        if(flag1==1):
            if (opc=="calculadora"): 
                tp1.Menu() 
                flag1=0
            if (opc=="graficadora"): 
                tp2.menu()
                flag1=0
            print()
            break