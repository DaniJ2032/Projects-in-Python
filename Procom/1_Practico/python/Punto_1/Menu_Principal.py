from bleach import clean
import Calculos_V1_0 as C 

def menu():
    
    print("CALCULADORA BASICA V1.0"); print("*"*25)
    print("1-Suma")
    print("2-Resta")
    print("3-Multiplica")
    print("4-Divide")
    print("5-Iteracion de operaciones")
    print("6-Salir del programa")
    print("*"*25)
    opc = int (input("Profavor elija una opcion del menu: "))
    Valuar(opc,0)

    if (opc == 1): C.Suma()
    if (opc == 2): C.Resta()
    if (opc == 3): C.Mult()
    if (opc == 4): C.Div()     
    if (opc == 5): menu2()

def Valuar(opc,opc2):
        
   while(opc>6):
        print("\n")
        print("*"*45)
        print("Opcion incorrecta, escoja una opcion entre (1) Y (5)")
        print("*"*45,"\n")
        opc = 0
        menu()
        print(opc, opc2)

   while(opc2>5):
        print("\n")
        print("*"*45)
        print("Opcion incorrecta, escoja una opcion entre (1) Y (4)")
        print("*"*45,"\n")
        opc2 = 0
        menu2()      

def menu2():

    print("\n")
    print ("*"*30)
    print("Menu de operaciones con iteracion")
    print("1-Suma")
    print("2-Resta")
    print("3-Multiplica")
    print("4-Volver a Menu Principal")
    print("5-salir del Programa")   
    print ("*"*30)
    opc2 = int (input("Ahora profavor elija una opcion del menu: "))
    Valuar(0,opc2) 

    if (opc2 == 1): C.Suma_itera()
    if (opc2 == 2): C.Resta_itera()
    if (opc2 == 3): C.Mult_itera()     
    if (opc2 == 4): opc2=0,menu()
