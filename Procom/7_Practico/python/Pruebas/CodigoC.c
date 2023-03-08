#include <stdio.h>
#include <string.h>
#include "xparameters.h"
#include "xil_cache.h"
#include "xgpio.h"
#include "platform.h"
#include "xuartlite.h"
#include "microblaze_sleep.h"

#define PORT_IN	 		XPAR_AXI_GPIO_0_DEVICE_ID //XPAR_GPIO_0_DEVICE_ID
#define PORT_OUT 		XPAR_AXI_GPIO_0_DEVICE_ID //XPAR_GPIO_0_DEVICE_ID

//Device_ID Operaciones
#define def_SOFT_RST            0
#define def_ENABLE_MODULES      1
#define def_LOG_RUN             2
#define def_LOG_READ            3

XGpio GpioOutput;
XGpio GpioParameter;
XGpio GpioInput;
u32 GPO_Value;
u32 GPO_Param;
XUartLite uart_module;

int main()
{
	init_platform();
	int Status;
	int indice = 0;
	int error  = 0;
	int flag_inicio = 0;
	XUartLite_Initialize(&uart_module, 0);
	
	GPO_Value=0x00000000;
	GPO_Param=0x00000000;
	unsigned char dato[4];
	
	Status=XGpio_Initialize(&GpioInput, PORT_IN);
	if(Status!=XST_SUCCESS){
		return XST_FAILURE;
	}
	Status=XGpio_Initialize(&GpioOutput, PORT_OUT);
	if(Status!=XST_SUCCESS){
		return XST_FAILURE;
	}
	XGpio_SetDataDirection(&GpioOutput, 1, 0x00000000);
	XGpio_SetDataDirection(&GpioInput, 1, 0xFFFFFFFF);
	
	u32  value;
	u32  byte_dato_low;
	u32  byte_dato_high;
	u32  resultado_dato;
	
	unsigned char datos;
	while(1){
		read(stdin,&dato[0],1);
		if (error != 1){
			switch (indice){
			case 0:
				if      (dato == 0xA2) 	{
					error = 0;
					flag_inicio = 1;
				}
				else if (dato == 0x00) 	{
					error = 0;
					flag_inicio = 1;
				}
				else if (dato == 0x00) 	{
					error = 0;
					flag_inicio = 1;
				}
				else if (dato == 0x01) 	{
					error = 0;
					flag_inicio = 1;
				}
				else error = 1;
				break;
			case 1:
				if (dato == 0x00) error = 0 ;
				else error = 1;
				break;
			case 2:
				if (dato == 0x00) error = 0 ;
				else error = 1;
				break;
			case 3:
				if (dato == 0x01) error = 0 ;
				else error = 1;
				break;
			case 4:
				if (dato == 0x02 || 0x04 || 0x09 || 0x00 ){
					byte_dato_high = dato;
					
				}
				else error = 1;
				
				break;
			case 5:
				if (dato == 0x49 || 0x92 || 0x24 || 0x01){
					byte_dato_low = dato;
					
				}
				else error = 1;
				
				break;
			case 6:
				if (dato == 0x42) error = 0;
				else error = 1;
				break;
			}
		}
		else{
			//enviar trama de error al python

			//XUartLite_Send(&uart_module, &(error),1);
			error       = 0;
			indice      = 0;
			flag_inicio = 0;
		}
		
		resultado_dato = (byte_dato_high << 8) + byte_dato_low;
		
		if (resultado_dato == 0x249 || 0x492 || 0x924){
			XGpio_DiscreteWrite(&GpioOutput,1, (u32) resultado_dato);
		}
		
		else if(resultado_dato == 0x001){
			
			XGpio_DiscreteWrite(&GpioOutput,1, (u32) 0x00000000);
			value = XGpio_DiscreteRead(&GpioInput, 1);
			salida=(char)(value&(0x0000000F));
			while(XUartLite_IsSending(&uart_module)){}
			XUartLite_Send(&uart_module, &(salida),1);
		
		}
		
		if (flag_inicio == 1) indice += 1;
		
		if 	(indice == 7){	
			indice = 0;
			flag_inicio = 0;
			error = 0;
		}

	}
	
	cleanup_platform();
	return 0;
}
