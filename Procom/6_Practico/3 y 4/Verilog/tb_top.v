/*Estimulos*/
`timescale 1ns/100ps

module tb_top ();

parameter NB_OUTPUT  = 8; //! NB of output
parameter NBF_OUTPUT = 6; //! NBF of output
parameter NB_COEFF   = 8; //! NB of Coefficients
parameter NBF_COEFF  = 6; //! NBF of Coefficients
parameter NBAUDS     = 6; //! Baudios del filtro 

//registros
reg                 i_reset;    
reg                 clock  ;   
reg           [3:0] i_sw   ; 
wire          [3:0] o_led  ; 

wire signed [NB_OUTPUT-1:0] tb_os_data;
wire [1:0] counter_to_FIR;

    //Initial 
    initial begin
        clock       =   1'b0   ;
        i_reset     =   1'b0   ;
        i_sw        =   4'b0000;
        //force tb_top.u_top_tx.u_prbsQI.i_enable = 0;
        //force tb_top.u_top_tx.u_BERandSLICER.i_enable = 0;
        #1000 i_reset =   1'b1   ;
        #1000 i_sw    =   4'b0011;
        //@(posedge clock);
        //force tb_top.u_top_tx.u_prbsQI.i_enable = 1;
        //#1000;
        //force tb_top.u_top_tx.u_BERandSLICER.i_enable = 1;
        #6000000   $finish     ;                        
    end
    
    //Clock
    always #5 clock = ~clock;    

    //Instancia del top
    top_tx
    #(
        .NB_OUTPUT  (NB_OUTPUT  ), //! NB of output
        .NBF_OUTPUT (NBF_OUTPUT ), //! NBF of output
        .NB_COEFF   (NB_COEFF   ), //! NB of Coefficients
        .NBF_COEFF  (NBF_COEFF  ), //! NBF of Coefficients
        .NBAUDS     (NBAUDS     ) //! Baudios del filtro 
    )
    u_top_tx
    (
        .i_reset    (i_reset),
        .clock      (clock  ),
        .i_sw       (i_sw   ),
        .o_led      (o_led  )
    );
  
endmodule