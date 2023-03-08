import numpy as np
import random as Rm
#  _________________________________________________________________________________________________
# |Funcion: Con data_plot() obtenemos los vectores de datos para cada plot del JoinVector           |
# |Recibe: una variable tipo 'int' indicando la cantidad maxima de subPlot que se tiene             |     
# |retorna:vectores para los datos del joinVector t,y0,numplot,show,typeGraf,xlim,ylim,xlabel,ylabel|
# |_________________________________________________________________________________________________| 
def data_plot(Max_SubPlot):
   
    numplot = input("Ingrese numero o titulo de cada plot: ").split(",")
    while Max_SubPlot != len(numplot):
        print("Error ingreso mas datos que los Plot disponibles para graficar")
        numplot = input("Vuelva a ingresar los datos porfavor: ").split(",")

    show = input("ingrese los graficos que quiere habilitar para ver colocando (True) o (False): ").split(",")
    while Max_SubPlot != len(show):
        print("Error ingreso mas datos que los Plot disponibles para graficar")
        show = input("Vuelva a ingresar los datos porfavor: ").split(",")

    typeGraf = input("Ingrese que tipo de graficos quiere escoja entre (Plot) o (Stem): ").split(",")
    while Max_SubPlot != len(typeGraf):
        print("Error ingreso mas datos que los Plot disponibles para graficar")
        typeGraf = input("Vuelva a ingresar los datos porfavor: ").split(",")

    xlim = eval(input("Ingrese los Limite de los ejes de X de c/u de los graficos: "))
    while Max_SubPlot != len(xlim):
        print("Error ingreso mas datos que los Plot disponibles para graficar")
        xlim = eval(input("Vuelva a ingresar los datos porfavor: "))

    ylim = eval(input("Ingrese los Limite de los ejes de y de c/u de los graficos: "))
    while Max_SubPlot != len(ylim):
        print("Error ingreso mas datos que los Plot disponibles para graficar")
        ylim = eval(input("Vuelva a ingresar los datos porfavor: "))

    xlabel = input("Ingrese identificador de los ejes x: ").split(",")
    while Max_SubPlot != len(xlabel):
        print("Error ingreso mas datos que los Plot disponibles para graficar")
        xlabel = input("Vuelva a ingresar los datos porfavor: ").split(",")

    ylabel = input("Ingrese identificador de los ejes y: ").split(",")
    while Max_SubPlot != len(ylabel):
        print("Error ingreso mas datos que los Plot disponibles para graficar")
        ylabel = input("Vuelva a ingresar los datos porfavor: ").split(",")

    x = [] #Vector de datos para el eje x
    y0 = [] #Vector de datos de y 

    for i in range(0,Max_SubPlot,1):         # Con el siguiente for() se crea los vectores t,y0 
        x.append(np.arange(0.,xlim[i],0.01)) # donde podemos almacenar funciones senos y cocenos en el vector y0
        funcion = Rm.choice(["sin","cos"])  
        if (funcion == 'sin'):
            y0.append(np.sin(2.*np.pi*Rm.choice([1.,2.,3.,4.])*x[i] + np.pi/Rm.choice([np.pi,1.,2.,0.75,0.5])))
        if (funcion == 'cos'):
            y0.append(np.cos(2.*np.pi*Rm.choice([1.,2.,3.,4.])*x[i] + np.pi/Rm.choice([np.pi,1.,2.,0.75,0.5])))
        
    return x,y0,numplot,show,typeGraf,xlim,ylim,xlabel,ylabel
