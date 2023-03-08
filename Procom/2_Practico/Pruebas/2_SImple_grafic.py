## Graficos usando matplotlib.pyplot
import numpy as np
import matplotlib.pyplot as pl

phase0 = 0.
phase1 = np.pi/2.
f0     = 2.
f1     = 2.
f2     = 4.

# t = np.arange(inicio, valor final,el paso)
t  = np.arange(0,f2,0.01)

y0 = np.sin(2.*np.pi*f0*t + phase0)
y1 = np.sin(2.*np.pi*f2*t + phase1)
y2 = np.cos(2.*np.pi*f2*t + phase0)
#y3 = np.ones((len(t),1))
pl.figure()
#pl.plot(t,y3)

pl.plot(t,y1,linewidth=1.0,label='Phase: %1.2f'%phase0)
#pl.plot(t,y0,linewidth=1.0,label='Phase: %1.2f'%phase0)
# pl.plot(t,y1,'o-',linewidth=1.0,label='Phase: %1.2f'%phase1)
#pl.plot(t,y2,'x-r',linewidth=1.0,label='Phase: %1.2f'%phase0)
# pl.stem(t,y2,label='Phase: %1.2f'%phase0)
#pl.axvline(x=1,color='k') #con esto se traza una linea vertical que pasa por X = 1 y le damos el color negro que es "K"
#pl.axvline(x=1.5,color='k')
#pl.axhline(y=1,color='k') #aca le decimos que trace una horizontal pasando por un punto en y = 1
pl.ylabel('Amplitud')
pl.xlabel('Tiempo')
pl.title('Seno-Coseno')
pl.legend()
pl.grid()
pl.show()