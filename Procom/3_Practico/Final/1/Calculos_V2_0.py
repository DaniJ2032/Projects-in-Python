import Pregunta as P
import numpy as np
"""Definiciones de funciones para los Calculos normales""" 
def Suma():
    a =  int(input("Valor del primer numero: "))
    b =  int(input("Valor del segundo numero: "))
    print()
    print("*"*40)
    print("EL resultado de la Suma es: ",a+b)
    print("*"*40,"\n")
    P.Pregunta()

def Resta():
    a =  int(input("Valor del primer numero: "))
    b =  int(input("Valor del segundo numero: "))
    print()
    print("*"*40)    
    print("EL resultado de la Resta es: ",a-b)
    print("*"*40,"\n")    
    P.Pregunta()

def Mult():
    a =  int(input("Valor del primer numero: "))
    b =  int(input("Valor del segundo numero: "))
    print()
    print("*"*40)    
    print("EL resultado de la Multiplicacion es: ",a*b)
    print("*"*40,"\n")    
    P.Pregunta()

def Div():
    a =  int(input("Valor del primer numero: "))
    b =  int(input("Valor del segundo numero: "))
    print()
    print("*"*40)    
    print("EL resultado de la Division es: ",a/b)
    print("*"*40,"\n")     
    P.Pregunta()
"""**********************************************"""

"""Definiciones de funciones para las Iteraciones"""
def Suma_itera():
    repite = int(input("Ingresa la cantidad de veces que desa iterar: "))
    paso = int(input("Ingresa el numero que desa iterar: "))
    print()
    total = 0
    for contador in range(repite):
        total += paso
    print("*"*40)   
    print("Resultado de la Suma Iterada es: ", total)
    print("*"*40,"\n")
    P.Pregunta()

def Resta_itera():
    repite = int(input("Ingresa la cantidad de veces que desa iterar: "))
    paso = int(input("Ingresa el numero que desa iterar: ")) 
    print()
    total = paso
    for contador in range(repite):
        total -= paso
    print("*"*40)    
    print("Resultado de la Resta Iterada es: ", total)
    print("*"*40,"\n")
    P.Pregunta()

def Mult_itera():
    repite = int(input("Ingresa la cantidad de veces que desa iterar: "))
    paso = int(input("Ingresa el numero que desa iterar: "))
    print()
    total = 1
    for contador in range(repite):
        total *= paso
    print("*"*40)    
    print("Resultado de la Multiplicacion Iterada es: ", total)
    print("*"*40,"\n")
    P.Pregunta()
"""********************************************************"""
   
"""Definiciones de Funciones para Producto Punto"""

def Vector():

    vector = []
    N = int(input("Ingrese el tamaño de los vectores: "))
    print("Ingrese datos del primer Vector:\n")
    for i in range(N):
        num = float(input("Elemento {}: ".format(i+1)))
        vector.append(num)
    a = vector
    print()
    print("*"*30)
    print("Vector (1): ",a)
    print("*"*30,"\n")

    print("Ingrese Datos del Segundo Vector:\n")
    vector2 = []
    for i in range(N):
        num = float(input("Elemento {}: ".format(i+1)))
        vector2.append(num)
    b = vector2
    print()
    print("*"*30)       
    print("Vector (2): ",b)
    print("*"*30,"\n")
    print("Producto Punto entre los vectores es:", np.dot(a,b))   
    P.Pregunta()

def Matriz():

    N = int(input("Ingresa cantidad de Filas: "))
    X = int(input("Ingresa cantidad de Columnas: "))
    print()

    matrizA = []
    print("Ingrese los datos de la primera matriz \n")
    for i in range (N):
        matrizA.append([])
        for j in range (X):
            valor = float(input("Fila {} Columna {} :".format(i+1, j+1)))
            matrizA [i].append(valor)
    print()
    print("*"*30)    
    print("Matriz (1):\n", np.matrix(matrizA))
    print("*"*30,"\n") 
    matrizB = []
    print("Ingrese los datos de la segunda matriz \n")
    for i in range (X):
        matrizB.append([])
        for j in range (N):
            valor = float(input("Fila {} Columna {} :".format(j+1, i+1)))
            matrizB [i].append(valor)
    print()
    print("*"*30)             
    print("Matriz (2):\n",np.matrix(matrizB))
    print("*"*30,"\n") 
    print("*"*30) 
    print("EL producto punto de las matrices es:\n",np.dot(matrizA,matrizB))
    print("*"*30,"\n")   
    P.Pregunta()
"""*********************************************************"""