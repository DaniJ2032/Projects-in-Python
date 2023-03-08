
"""Definiciones de funciones para los Calculos normales""" 
def Suma():
    a =  int(input("Valor del primer numero: "))
    b =  int(input("Valor del segundo numero: "))
    print("\n")
    print("*"*40)
    print("EL resultado de la Suma es: ",a+b)
    print("*"*40,"\n")


def Resta():
    a =  int(input("Valor del primer numero: "))
    b =  int(input("Valor del segundo numero: "))
    print("\n")
    print("*"*40)    
    print("EL resultado de la Resta es: ",a-b)
    print("*"*40,"\n")    


def Mult():
    a =  int(input("Valor del primer numero: "))
    b =  int(input("Valor del segundo numero: "))
    print("\n")
    print("*"*40)    
    print("EL resultado de la Multiplicacion es: ",a*b)
    print("*"*40,"\n")    


def Div():
    a =  int(input("Valor del primer numero: "))
    b =  int(input("Valor del segundo numero: "))
    print("\n")
    print("*"*40)    
    print("EL resultado de la Division es: ",a/b)
    print("*"*40,"\n")     
"""**********************************************"""

"""Definiciones de funciones para las Iteraciones"""
def Suma_itera():
    repite = int(input("Ingresa la cantidad de veces que desa iterar: "))
    paso = int(input("Ingresa el numero que desa iterar: "))
    print("\n")
    total = 0
    for contador in range(repite):
        total += paso
    print("*"*40)   
    print("Resultado de la Suma Iterada es: ", total)
    print("*"*40,"\n")


def Resta_itera():
    repite = int(input("Ingresa la cantidad de veces que desa iterar: "))
    paso = int(input("Ingresa el numero que desa iterar: ")) 
    print("\n")
    total = paso
    for contador in range(repite):
        total -= paso
    print("*"*40)    
    print("Resultado de la Resta Iterada es: ", total)
    print("*"*40,"\n")


def Mult_itera():
    repite = int(input("Ingresa la cantidad de veces que desa iterar: "))
    paso = int(input("Ingresa el numero que desa iterar: "))
    print("\n")
    total = 1
    for contador in range(repite):
        total *= paso
    print("*"*40)    
    print("Resultado de la Multiplicacion Iterada es: ", total)
    print("*"*40,"\n")
"""********************************************************"""
   
