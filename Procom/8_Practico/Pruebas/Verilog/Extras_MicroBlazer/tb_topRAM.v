//////////////////////////////////////////////////////////////////////////////////
// AUTOR: Jose gomez Lazarte, Juarez Daniel 
// AÑO:   2023  
// NOMBRE: Módulo TB de prueba para la RAM 
//
//////////////////////////////////////////////////////////////////////////////////

`timescale 1ns/100ps

  
module tb_top ();

parameter RAM_WIDTH       = 32;            
parameter RAM_DEPTH       = 32;                  
parameter RAM_PERFORMANCE = "LOW_LATENCY";
parameter INIT_FILE       = "";


////registros
//reg                 i_reset;    
//reg                 clock  ;   
//reg           [3:0] i_sw   ; 
//wire          [3:0] o_led  ; 
reg [clogb2(RAM_DEPTH-1)-1:0] WriteAdress ;
reg [clogb2(RAM_DEPTH-1)-1:0] ReadAdress  ;
reg [RAM_WIDTH - 1:0]         Dato_input  ;
reg                           clock       ;
reg                           Write_enable;
reg                           Read_Enable ;
wire [RAM_WIDTH-1:0]          Dato_output ;
//wire signed [NB_OUTPUT-1:0] tb_os_data;
//wire [1:0] counter_to_FIR;

    //Initial 
    initial begin
        clock       =   1'b0   ;
        //i_reset     =   1'b0   ;
        //i_sw        =   4'b0000;
        //force tb_top.u_top_tx.u_prbsQI.i_enable = 0;
        //force tb_top.u_top_tx.u_BERandSLICER.i_enable = 0;
        //#1000 i_reset =   1'b1   ;
        //#1000 i_sw    =   4'b0011;
        //@(posedge clock);
        //force tb_top.u_top_tx.u_prbsQI.i_enable = 1;
        //#1000;
        //force tb_top.u_top_tx.u_BERandSLICER.i_enable = 1;
        #6000000   $finish     ;                        
    end
    
    //Clock
    always #5 clock = ~clock;    

    //Instancia del top
    BlockRAM
    #(
        .RAM_WIDTH      (RAM_WIDTH      ),
        .RAM_DEPTH      (RAM_DEPTH      ),
        .RAM_PERFORMANCE(RAM_PERFORMANCE), 
        .INIT_FILE      (INIT_FILE      )
        
    )
    u_BlockRAM
    (
        .WriteAdress  (WriteAdress  ),
        .ReadAdress   (ReadAdress   ),
        .Dato_input   (Dato_input   ),
        .clock        (clock        ),
        .Write_enable (Write_enable ),
        .Read_Enable  (Read_Enable  ),
        .Dato_output  (Dato_output  )
    );

function integer clogb2;
    input integer depth;
      for (clogb2=0; depth>0; clogb2=clogb2+1)
        depth = depth >> 1;
endfunction  
endmodule