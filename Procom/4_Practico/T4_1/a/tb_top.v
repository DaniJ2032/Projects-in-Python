/*_____TP_4_Punto_A Instancia de modulos para leds_______
*Autor: Daniel Juarez                                    *                  
*Fecha: 04/06/2021                                       *
*________________________________________________________*
*/
//Estimulos
`timescale 1ns/100ps

module tb_top ();

    //Parameters
    parameter   NB_SW       = 4;
    parameter   NB_BTN      = 4;
    parameter   NB_COUNTER  = 16;
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
        
        //prueba en modo flash

        #10000     i_btn   =  4'b0010; //selecciono Azul
        #5000      i_btn   =  4'b0000; 
        
        #200000    i_sw    =  4'b0101; //activo el contador
        #200000    i_sw    =  4'b0101; //selecciono velocidad 

        #10000     i_btn   =  4'b0100; //selecciono rojo
        #5000      i_btn   =  4'b0000;

        #200000    i_sw    =  4'b0011; //cambio de velocidad
        #200000    i_sw    =  4'b0011;

        #10000     i_btn   =  4'b1000; //selecciono verde
        #5000      i_btn   =  4'b0000;

        #200000    i_sw    =  4'b0111; //Ultimo cambio de velocidad        
        #200000    i_sw    =  4'b0111; //
//////////////////////////////////////////////

        // Prueba de barrido

        #10000     i_btn   =  4'b0001;
        #5000      i_btn   =  4'b0000; //modo shift        
                 
        #200000    i_sw    =  4'b0101; //Barrido de der a izq
        #200000    i_sw    =  4'b0101; // seteo de velocidad
        #200000    i_sw    =  4'b1101; //Barrido de izq a der

        #200000    i_sw    =  4'b0101; //Barrido de der a izq
        #10000     i_btn   =  4'b0010; //selecciono Azul
        #5000      i_btn   =  4'b0000;

        #200000    i_sw    =  4'b0011; //
        #200000    i_sw    =  4'b0011; //cambio de velocidad
        #200000    i_sw    =  4'b1011; //cambio de barrido

        #200000    i_sw    =  4'b0011; 
        #10000     i_btn   =  4'b0100; //selecciono rojo
        #5000      i_btn   =  4'b0000;
        #200000    i_sw    =  4'b1011; //cambio de barrido

        #200000    i_sw    =  4'b0111; //Ultimo cambio de velocidad 
        #10000     i_btn   =  4'b1000; //selecciono verde
        #5000      i_btn   =  4'b0000;
        #200000    i_sw    =  4'b1111; //Ultimo cambio de barrido 
 
        #5000      i_reset   =  1'b0; //reseteo
        #5000      i_reset   =  1'b1; 

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
