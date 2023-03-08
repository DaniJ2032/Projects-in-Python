/*_____TP_4_Punto_A Instancia de modulos para leds_______
*Autor: Daniel Juarez                                    *                  
*Fecha: 04/06/2021                                       *
*________________________________________________________*
*/
module flashReg
#(parameter NB_LEDS = 4)  
(
    output  [NB_LEDS-1:0] o_FS_led, //salida del flashreg       
    input   i_valid,                //señal de validacion
    input   i_reset,               
    input   clock                  
);

//Variables
reg [NB_LEDS-1:0] flashReg;

//Descripcion del flashReg
always @(posedge clock)begin

    if(i_reset) begin   
        flashReg <= 4'b1111; //reseteo del flash por defecto todos los led prendidos
    end    

    else if(i_valid) begin
        flashReg <= ~flashReg;  //Togleo el registro del flash
    end    

    else begin
        flashReg <= flashReg;   //no genero cambios si no hay pulso de relog
    end    
end //fin de always()    

//Salida
    assign o_FS_led = flashReg; //señal de salida del modulo flashreg

endmodule