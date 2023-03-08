/*_____TP_4_Punto_B Agregamos un 3er barrido de leds______
*Autor: Daniel Juarez                                    *                  
*Fecha: 04/06/2021                                       *
*________________________________________________________*
*/
module flashReg
#(parameter NB_LEDS = 4)  
(
    output  [NB_LEDS-1:0] o_FS_led, 
    output  o_valid,                //salida de validacion para el ShiftReg2Led       
    input   i_valid,                //validacion de entrada
    input   i_reset,                //reset global
    input   clock                   //señal de clock
);

//Registros
reg [NB_LEDS-1:0] flashReg;
reg o_valid_reg;

//Descripcion del flashreg.
always @(posedge clock)begin

    if(i_reset) begin   
        flashReg <= 4'b1111; //reseteo del flash todos los led encendidos por defecto
    end    
    
    else begin
     o_valid_reg <= 1'b1;   //se manda una señal de validacion a la salida
    
         if(i_valid) begin
        
            flashReg <= ~flashReg;  //Togleo el registro del flash
         end    
        else begin
            flashReg <= flashReg;   //no genero cambios si no hay pulso de relog
            o_valid_reg <= o_valid_reg;
        end 
    end   
end //fin de always()    

//Salidas
assign o_FS_led = flashReg;
assign o_valid = o_valid_reg; 
      
endmodule