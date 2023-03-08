/*_____TP_4_Punto_B Agregamos un 3er barrido de leds______
*Autor: Daniel Juarez                                    *                  
*Fecha: 04/06/2021                                       *
*________________________________________________________*
*/
module shiftreg
#(  parameter NB_LEDS = 4 )  
(
    output  [NB_LEDS-1:0] o_SR_led,  //salida para los 4 led del ShiftReg 
    output  o_valid,                 //salida de la señal de validacion
    
    input   i_sw,                    //NB_SW[3]  Para seleccion de direccion de barrido
    input   i_btn,       
    input   i_valid,                 //señal de validacion
    input   i_reset,                 //reset global
    input   clock                    //señal de clock
);

//Registros
reg [NB_LEDS-1:0] shiftreg;
reg o_valid_reg;
reg reg_btn; 
reg [1:0]count; 


//Decripcion del shifter.
always @(posedge clock)begin

    if(i_reset) begin           //si tenemos reset
        reg_btn      <= 1'b0; 
        count        <= 2'b00;
        shiftreg     <= 4'b0001; //reseteo del shifter               
  
    end 
    else begin
    
        //conteo del boton
        reg_btn <= i_btn;    
        if(reg_btn == 1'b0 && i_btn == 1'b1)
            count <= count + 2'b01; //incremento el contador
        else if(count == 2'b11)
            count <= 2'b00;         //reseteo el contado
        else 
            count <= count;

        if (i_valid == 1'b1)begin
            o_valid_reg <=1'b1;     //validacion a la salida

            if (i_sw == 1'b0 && count == 2'b01) begin 

                shiftreg <= {shiftreg[NB_LEDS-2:0],shiftreg[3]}; //concateno la salida desde el led R0 al R3
                
            end
            else if (i_sw == 1'b1 && count == 2'b01) begin 

                shiftreg <= {shiftreg[0],shiftreg[NB_LEDS-1:1]}; //concateno la salida desde el led R3 a R0
            end

            else begin
                shiftreg <= shiftreg;   //no genero cambios      
            end
        end
        else 
            o_valid_reg <= o_valid_reg; //no genero cambios
    end //fin de else   
end //fin del always    

//Salidas
    assign  o_SR_led = shiftreg;
    assign  o_valid = o_valid_reg;

endmodule