/*_____TP_4_Punto_B Agregamos un 3er barrido de leds______
*Autor: Daniel Juarez                                    *                  
*Fecha: 04/06/2021                                       *
*________________________________________________________*
*/
/*Estimulos*/
`timescale 1ns/100ps

module tb_top ();

    //Parameters
    parameter   NB_SW       = 4;
    parameter   NB_BTN      = 4;
    parameter   NB_COUNTER  = 16;   //se coloca en 16 el valor para visualizar los cambios
    parameter   NB_LEDS     = 4;

    //Vars
    wire [NB_LEDS-1 : 0] o_led  ;  
    wire [NB_LEDS-1 : 0] o_led_b;   
    wire [NB_LEDS-1 : 0] o_led_g;
    wire [NB_LEDS-1 : 0] o_led_r;
    
    reg [NB_SW-1  : 0]  i_sw   ;
    reg [NB_BTN-1 : 0]  i_btn  ;
    reg                 i_reset;    
    reg                 clock  ;        

    //Initial 
    initial begin
        clock       =   1'b0   ;
        i_reset     =   1'b0   ;
        i_sw        =   4'b0000;
        i_btn       =   4'b0000;
        #40 i_reset =   1'b1   ;
        
        // Prueba de botones

        #10000     i_btn = 4'b0001;
        #5000      i_btn = 4'b0000; //modo shiftreg  count = 1        
        #10000     i_sw  = 4'b0001; //activo el contador

        #1600000   i_sw  = 4'b0001; //Barrido por defecto de izq a derecha 
        #1600000   i_sw  = 4'b1001; //Barrido de dercha a izquierda
        #1600000   i_sw  = 4'b1001; //Barrido de dercha a izquierda 
        ///////////////////////////

        #10000     i_btn = 4'b0001; // count = 2
        #5000      i_btn = 4'b0000; //modo shiftreg2Led        

        #1600000   i_sw  = 4'b1001; //Barrido desde el centro 
        #1600000   i_sw  = 4'b0001; //Barrido desde los extremos
        #1600000   i_sw  = 4'b0001; //Barrido de dercha a izquierda 
        ///////////////////////////

        #10000     i_btn = 4'b0001; //reseteo el contador en count = 3
        #5000      i_btn = 4'b0000;        
        
        #800000    i_sw  = 4'b0001; //reinicio al modo flash

        #6000000   $finish;                        
    end
    
    //Clock
    always #5 clock = ~clock;    

    top
    #(
        .NB_SW      (NB_SW),
        .NB_BTN     (NB_BTN),   
        .NB_COUNTER (NB_COUNTER),
        .NB_LEDS    (NB_LEDS)
    )

    u_top
    (
        .o_led   (o_led  ),
        .o_led_b (o_led_b),
        .o_led_g (o_led_g),
        .o_led_r (o_led_r),     
        .i_sw    (i_sw   ),
        .i_btn   (i_btn  ),
        .i_reset (i_reset),
        .clock   (clock  )
    );
  
endmodule