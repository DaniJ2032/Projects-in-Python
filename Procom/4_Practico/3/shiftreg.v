/*MODULO SHIFTER */
module shiftreg
#(  parameter NB_LEDS = 4   )  
(
    output  [NB_LEDS-1:0] o_led,    //salida para los 4 led del ShiftReg        
    input   i_valid,                //señal de validacion
    input   i_reset,                //reset global
    input   clock                   //señal de clock
);

//Vaariables
reg [NB_LEDS-1:0] shiftreg;
//integer ptr;

//shifter descrip.
always @(posedge clock)begin

    if(i_reset) begin   //si tenemos reset
        shiftreg <= 4'b0001; //reseteo del shifter  
    end    

    else if (i_valid == 1'b1) begin //Cuando la señal de validacion proveniente del comparador junto con el count es 1
        // shiftreg <= shiftreg <<1;
        // shiftreg <= shiftreg[3] //Una forma de realizar un corrimiento

        // shiftreg[1] <= shiftreg[0]
        // shiftreg[2] <= shiftreg[1] //2da forma de manera manual
        // shiftreg[3] <= shiftreg[2]
        // shiftreg[0] <= shiftreg[3]

        // for (ptr=0; ptr<3; ptr=ptr+1) begin //3a forma con el uso de un for
        //     shiftreg[ptr+1] <= shiftreg[ptr]
        // end     
        // shiftreg[0] <= shiftreg[3]

        // //Metodo de concatenado (4 maneras de descripcion)
        // shiftreg <= {shiftreg[2:0],shiftreg[3]}
        // shiftreg <= {shiftreg[NB_LEDS-2:0],shiftreg[NB_LEDS-1]}
        // shiftreg <= {shiftreg[2-:3],shiftreg[3]}
        shiftreg <= {shiftreg[NB_LEDS-2 -: NB_LEDS-1],shiftreg[NB_LEDS-1]}; //concateno la salida desde el led R0 al R3
    end    

    else begin
        shiftreg <= shiftreg;   //no genero cambios si no hay pulso de relog
    end    
end //fin de always()    

//Salida
    assign o_led = shiftreg;

endmodule