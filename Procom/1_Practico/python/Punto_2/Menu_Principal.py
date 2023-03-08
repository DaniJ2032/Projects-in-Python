import Calculos_V2_0 as C 
import Pregunta as P

def Menu():
    
    print("CALCULADORA BASICA V1.0"); print("*"*25)
    print("1-Suma")
    print("2-Resta")
    print("3-Multiplica")
    print("4-Divide")
    print("5-Iteracion de operaciones")
    print("6-Producto Punto de Matrices y Vectores")
    print("7-Salir del programa")
    print("*"*25)
    opc = int (input("Profavor elija una opcion del menu: "))
    P.Valuar(opc,0,0)

    if (opc == 1): C.Suma()
    if (opc == 2): C.Resta()
    if (opc == 3): C.Mult()
    if (opc == 4): C.Div()  
    if (opc == 5): Menu2()   
    if (opc == 6): MenuPunto()

def Menu2():

    print()
    print ("*"*30)
    print("Menu de operaciones con iteracion")
    print("1-Suma")
    print("2-Resta")
    print("3-Multiplica")
    print("4-Volver a Menu Principal")
    print("5-salir del Programa")   
    print ("*"*30)
    opc2 = int (input("Ahora profavor elija una opcion del menu: "))
    P.Valuar(0,opc2,0) 

    if (opc2 == 1): C.Suma_itera()
    if (opc2 == 2): C.Resta_itera()
    if (opc2 == 3): C.Mult_itera()     
    if (opc2 == 4): Menu()

def MenuPunto():

    print()
    print("*"*30)
    print("Opciones de Producto Punto")
    print("1-Vectores")
    print("2-Matrices")
    print("3-Volver al Menu Principal")
    print("4-Salir del Programa")
    print("*"*30)
    opc3 = int (input("Profavor elija una opcion del menu: "))
    P.Valuar(0,0,opc3) 

    if (opc3 == 1): C.Vector()
    if (opc3 == 2): C.Matriz()
    if (opc3 == 3): Menu()     

