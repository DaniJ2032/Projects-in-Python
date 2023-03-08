//////////////////////////////////////////////////////////////////////////////////
// AUTOR: Jose gomez Lazarte, Juarez Daniel 
// AÑO:   2023  
// NOMBRE: Módulo Logue para manejo de lectura y escritura de la block RAM  
//
//////////////////////////////////////////////////////////////////////////////////

module logeo(
  input         clock      ,
  input         En_logeo   ,
  input  [31:0] i_adress   ,
  input         En_read    ,
  input  [31:0] datos_input,
  input         i_reset    ,
  output [31:0] o_dato
);

  parameter RAM_WIDTH       = 32           ;            
  parameter RAM_DEPTH       = 32000        ;                  
  parameter RAM_PERFORMANCE = "LOW_LATENCY";
  parameter INIT_FILE       = ""           ; 
  
  reg [15:0] counter_adress;
  reg        enable_counter; 
  
  wire Write_enable;

  ///////////////////////////////////////////
  // BlockRAM
  ///////////////////////////////////////////
  BlockRAM
  #(
      .RAM_WIDTH       (RAM_WIDTH      ),               
      .RAM_DEPTH       (RAM_DEPTH      ),                     
      .RAM_PERFORMANCE (RAM_PERFORMANCE),
      .INIT_FILE       (INIT_FILE      )                            
   )
   u_RAM
    (.WriteAdress (counter_adress),
     .ReadAdress  (i_adress      ),
     .Dato_input  (datos_input   ),
     .clock       (clock         ),
     .Write_enable(Write_enable  ),
     .Read_Enable (En_read       ),
     .Dato_output (o_dato        ) 
    );
  ////////////////////////////////////

  always @(posedge clock) begin
    if(i_reset == 1'b1) begin
        counter_adress <= 16'b0;
        enable_counter <= 1'b0 ;
    end
    else begin
        if (En_logeo)begin
                if (counter_adress < 16'b0111110100000000) counter_adress <= counter_adress + 1'b1;
                else begin 
                    counter_adress <= counter_adress;
                    enable_counter <= 1'b0;
                end
            end
            else if(En_read == 1'b0) begin
                counter_adress <= 16'b0;
                enable_counter <= 1'b1;
            end
    end
  end

assign Write_enable = En_logeo & enable_counter; //and para el enable de escritura BlockRAM
endmodule
