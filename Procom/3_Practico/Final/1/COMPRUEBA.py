#  ______________________________________________________________________________________________________________
# |Funcion: Comprueba() encargada de realizar la comprobacion de que el JoinVector se ingreso de manera correcta |
# |Recibe: fila,columna,matriz,JoinVector                                                                        | 
# |retorna: variable Warning con un 0 o un 1 indicando si hubo un error en la comprobacion o no                  |                                                                                | 
# |______________________________________________________________________________________________________________|

def Comprueba (fila,columna,matriz,JoinVector):

    warning = 0
    Colum_Init  = [1]
    Colum_Final = []
    
    for i in range (columna):               
        if i == 0:
            Colum_Init = [fila[i] for fila in matriz]   # Obtengo las columnas de los extremos de la matriz para comprobacion
        if i==(columna-1):
            Colum_Final = [fila[i] for fila in matriz] 
            break

    for i in range(len(JoinVector)):

        if isinstance(JoinVector[i], tuple):
            if ((columna*fila) < JoinVector[i][0]):  # Compruebo que en algun lugar de las agrupaciones
                print(JoinVector[i][0])              # o valiores individuales no se ingreso un valor mayor a lo permitido en la matriz   
                warning = 1                          # ej: matriz de 9 elemenos no puede haber un 10 en los datos  
                break

            if ((columna*fila) < JoinVector[i][1]):
                print(JoinVector[i][1])
                warning = 1
                break  

        if isinstance(JoinVector[i], int):
            if ((columna*fila) < (JoinVector[i])):
                warning = 1
                break

    for i in range(0,len(JoinVector), 1): 

        if isinstance(JoinVector[i], int):
            if (JoinVector[i] == JoinVector[i+1]):  #Evitamos valores repetidos individuales ej: 4,4
                warning = 2
                break

            if isinstance(JoinVector[i+1], (tuple)):
                if ((JoinVector[i+1][0]) < JoinVector[i]): # Evitamos repeticiones entre valores singulares 
                    warning = 3                            # y agrupaciones ej: 4,(4,6)    
                    break       

        if isinstance(JoinVector[i], tuple): 
            if (JoinVector[i][0] > JoinVector[i][1]):
                warning = 4                             # verifico si el primer valor no es mayor al siguiente
                break                                   # dentro de una agrupacion ej: (6,5)

            for valor in range(JoinVector[i][0] + 1 , JoinVector[i][1] - 1):  # comprobacion de valores intermedios
                for valor2 in Colum_Final:                                    # ej:(2,5) comprobacion que empiece en 2 y termine en 5
                    if valor == valor2:                                      
                        warning = 5
                        break                                                              
    return warning                     

                

                            
                    
