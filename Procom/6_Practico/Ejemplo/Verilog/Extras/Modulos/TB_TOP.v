/*Estimulos*/
`timescale 1ns/100ps

module tb_top ();

    reg                 i_reset;    
    reg                 clock  ;        

    //Initial 
    initial begin
        clock       =   1'b0   ;
        i_reset     =   1'b0   ;
        #40 i_reset =   1'b1   ;
        
        // Prueba de botones

        // #10000     i_btn = 4'b0001;
        // #5000      i_btn = 4'b0000; //modo shiftreg  count = 1        
        // #10000     i_sw  = 4'b0001; //activo el contador

        // #1600000   i_sw  = 4'b0001; //Barrido por defecto de izq a derecha 
        // #1600000   i_sw  = 4'b1001; //Barrido de dercha a izquierda
        // #1600000   i_sw  = 4'b1001; //Barrido de dercha a izquierda 
        // ///////////////////////////

        // #10000     i_btn = 4'b0001; // count = 2
        // #5000      i_btn = 4'b0000; //modo shiftreg2Led        

        // #1600000   i_sw  = 4'b1001; //Barrido desde el centro 
        // #1600000   i_sw  = 4'b0001; //Barrido desde los extremos
        // #1600000   i_sw  = 4'b0001; //Barrido de dercha a izquierda 
        // ///////////////////////////

        // #10000     i_btn = 4'b0001; //reseteo el contador en count = 3
        // #5000      i_btn = 4'b0000;        
        
        // #800000    i_sw  = 4'b0001; //reinicio al modo flash

        #6000000   $finish;                        
    end
    
    //Clock
    always #5 clock = ~clock;    

    TX_top
    u_TX_top
    (
        .i_reset (i_reset),
        .clock   (clock  )
    );
  
endmodule