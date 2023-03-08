#  ______________________________________________________________________________________________________________
# |Funcion: Error() Encargada de señalar el error cometido a la hora de ingresar las agrupaciones en JoinVector  |
# |Recibe: una variable "opcion" la cual en vase al valor indica que error se cometio                            | 
# |retorna: nada                                                                                                 | 
# |______________________________________________________________________________________________________________|
def Error(opcion):

    while(opcion !=0):

        if((opcion == 1)): 
            print("*",60)
            print("Error: uno o varios valores ingresados fuera del rango de la matriz")  
            print("*",60)
            break
        if((opcion == 2)): 
            print("*",60)
            print("Error: uno o varios valores individuales repetidos entre si")
            print("*",60)
            break
        if((opcion == 3)): 
            print("*",60)
            print("Error: uno o varios valores repetidos entre valores individuales y agrupaciones")
            print("*",60)
            break
        if((opcion == 4)): 
            print("*",60)
            print("Error: uno o valrios valores iniciales en las agrupaciones son mas grande que el siguiente valor")
            print("*",60)
            break
        if((opcion == 5)): 
            print("*",60)
            print("Error: algun valor de agrupacion supera el limite por fila de las matriz de impresion")
            print("*",60)
            break



