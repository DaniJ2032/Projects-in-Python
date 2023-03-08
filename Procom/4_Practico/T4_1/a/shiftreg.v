/*_____TP_4_Punto_A Instancia de modulos para leds_______
*Autor: Daniel Juarez                                    *                  
*Fecha: 04/06/2021                                       *
*________________________________________________________*
*/
module shiftreg
#( parameter NB_LEDS = 4 )  
(
    output  [NB_LEDS-1:0] o_SR_led,  
    output  o_valid,                 //salida de la señal de validacion
    
    input   i_sw,                    //NB_SW[3]  Para seleccion de direccion de barrido       
    input   i_valid,                 //validaciond e entrada
    input   i_reset,                 //reset global
    input   clock                    //señal de clock
);

//Registros
reg [NB_LEDS-1:0] shiftreg;
reg o_valid_reg;    

//Descripcion del shiftreg.
always @(posedge clock)begin

    if(i_reset) begin   //si tenemos reset
        shiftreg <= 4'b0001; //reseteo del shifter  
    end    
    else if (i_valid == 1'b1 && i_sw == 1'b0) begin

        shiftreg <= {shiftreg[NB_LEDS-2:0],shiftreg[3]}; //salida desde el led R0 al R3
        o_valid_reg <= 1'b1;
    end
    else if (i_valid == 1'b1 && i_sw == 1'b1) begin

        shiftreg <= {shiftreg[0],shiftreg[NB_LEDS-1:1]}; //salida desde el led R3 a R0
        o_valid_reg <= 1'b1;
    end
    else begin
        shiftreg <= shiftreg;   //no genero cambios si no hay pulso de relog
        o_valid_reg <= o_valid_reg;
    end    
end //fin de always()    

//Salidas
    assign o_SR_led = shiftreg;
    assign  o_valid = o_valid_reg;

endmodule