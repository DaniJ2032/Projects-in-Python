#Multiples graficos 
#metodo de sub plot como en MatLab
import numpy as np
import matplotlib.pyplot as pl

phase0 = 0.
phase1 = np.pi*3./4.
f0     = 2.
f1     = 2.
f2     = 4.

t  = np.arange(0,4,1)
print(phase1)
#rand 1<m<4
#if(1)
# x funcion(variales) --> fijas , rand pára las variables   wo = 2*pi*frec
# rand frecuencia y fase 
y0 = np.sin(2.*np.pi*f0*t + phase1)
y1 = np.cos(2.*np.pi*f1*t + phase1)
y2 = np.cos(2.*np.pi*f2*t + phase0)

print(y0)


pl.figure(figsize=[13,13])
#le pasamos cantida de filas, cantidad de columnas y posicion del grafico


pl.subplot(3,3,1)
pl.plot(t,y0,'.-',linewidth=2.0,label='Phase: %1.2f'%phase0)
pl.ylabel('Amplitud')
pl.xlabel('Tiempo')
pl.legend()
pl.grid()

pl.subplot(3,3,(2,3))
pl.plot(t,y0,'.-',linewidth=2.0,label='Phase: %1.2f'%phase0)
pl.ylabel('Amplitud')
pl.xlabel('Tiempo')
pl.legend()
pl.grid()

pl.subplot(3,3,(4,7))
pl.plot(t,y1,'rx-',linewidth=1.0,label='Phase: %1.2f'%phase1)
pl.ylabel('Amplitud')
pl.xlabel('Tiempo')
pl.legend()
pl.grid()


pl.subplot(3,3,5)
pl.stem(t,y2,'y',markerfmt='v')
pl.plot(t,y2,'g',linewidth=1.0,label='Phase: %1.2f'%phase0)
pl.ylabel('Amplitud')
pl.xlabel('Tiempo')
pl.xlim(0,0.5)
pl.legend()
pl.grid()
pl.show()

pl.subplot(3,3,6)
pl.plot(t,y1,'.',linewidth=1.0,label='Phase: %1.2f'%phase1)
pl.ylabel('Amplitud')
pl.xlabel('Tiempo')
pl.legend()
pl.grid()


pl.subplot(3,3,(8,9))
pl.plot(t,y1,'m+-',linewidth=1.0,label='Phase: %1.2f'%phase1)
pl.ylabel('Amplitud')
pl.xlabel('Tiempo')
pl.legend()
pl.grid()
pl.title('Sin')


## Guardando figuras en archivos
# pl.savefig('grafica.eps')
# pl.savefig('grafica.pdf')
# pl.savefig('grafica.png')

