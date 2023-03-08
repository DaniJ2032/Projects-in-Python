import matplotlib.pyplot as pl
import random as rm
import SHOWGRAFIC as sg
#  ____________________________________________________________________________________________________________
# |Funcion: figplot() es la encargada de realizar la impresion de los subPlot en nuestra area matriz de trabajo|
# |Recibe: Los parametros para realizar los multiples SubPlot                                                  | 
# |retorna: nada                                                                                               | 
# |____________________________________________________________________________________________________________|

def figplot(x, y0, filas, columnas, JoinVector, numplot, show, typeGraf, xlim, ylim, xlabel, ylabel):

    # La siguiente liena de codigo lo que realiza es un descarte en base a que SubPlot se les coloco "false"    
    x2,y2,JoinVector2,numplot2,typeGraf2,xlim2,ylim2,xlabel2,ylabel2,Colum_Init=sg.show_grafic(x,y0,filas,columnas,JoinVector,numplot,show,typeGraf,xlim,ylim,xlabel,ylabel)

    pl.figure(figsize=[14,14]) #tamaño de las figuras dentro de la matriz de impresion 

    for j in range(0,len(JoinVector2), 1): #recorro cada JoinVecor y le asigno todos sus valores

        pl.subplot(filas,columnas,JoinVector2[j])
        pl.ylim(-ylim2[j],+ylim2[j])
        pl.xlim(0,+xlim2[j])

        if typeGraf2[j] == "plot":
            pl.plot(x2[j],y2[j],rm.choice(["r", "b", "g", "k", "c", "m", "y", "violet"]),linewidth=2.0)
        
        if typeGraf2[j] == "stem":
            pl.stem(x2[j],y2[j],rm.choice(["r", "b", "g", "k", "c", "m", "y", "violet"]),markerfmt='x')
        
        if isinstance(JoinVector2[j], int):
            for Valor in Colum_Init:
                if Valor == JoinVector2[j]:
                    pl.ylabel(ylabel2[j])
                    break

        if isinstance(JoinVector2[j], tuple):
            for Valor in Colum_Init:
                if Valor == JoinVector2[j][0]:
                    pl.ylabel(ylabel2[j])
                    break                                     
        
        if isinstance(JoinVector2[j], int):
            if JoinVector2[j] == ((filas*columnas)-(columnas-1)):
                pl.xlabel(xlabel2[j]) 
        
        if isinstance(JoinVector2[j], tuple):
            if JoinVector2[j][0] == ((filas*columnas)-(columnas-1)):
                pl.xlabel(xlabel2[j]) 

        pl.title(numplot2[j])

    pl.show()    #muestro todos los plot de "true"
    pl.grid()    
    #fin de funcion figplot()

 
