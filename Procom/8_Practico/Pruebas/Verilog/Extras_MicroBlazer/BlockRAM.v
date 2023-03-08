//////////////////////////////////////////////////////////////////////////////////
// AUTOR: Jose gomez Lazarte, Juarez Daniel 
// AÑO:   2023  
// NOMBRE: Block RAM de 32kb para almacenamiento de datos de los filtros 
//
//////////////////////////////////////////////////////////////////////////////////
  
module BlockRAM
  #(
      parameter RAM_WIDTH       = 32           ,            
      parameter RAM_DEPTH       = 32000        ,                  
      parameter RAM_PERFORMANCE = "LOW_LATENCY",
      parameter INIT_FILE       = ""                       
   )
   (
    input [15:0] WriteAdress ,
    input [15:0] ReadAdress  ,
    input [RAM_WIDTH - 1:0]         Dato_input  ,
    input                           clock       ,
    input                           Write_enable,
    input                           Read_Enable ,
    output [RAM_WIDTH-1:0]          Dato_output 
    
    
    );
    
  reg [RAM_WIDTH-1:0] BlockRAM [RAM_DEPTH-1:0];
  reg [RAM_WIDTH-1:0] RAM_DATA = {RAM_WIDTH{1'b0}};
  
  wire rstb  ;
  wire regceb;
  
  // The following code either initializes the memory values to a specified file or to all zeros to match hardware
  generate
    if (INIT_FILE != "") begin: use_init_file
      initial
        $readmemh(INIT_FILE, BlockRAM, 0, RAM_DEPTH-1);
    end else begin: init_bram_to_zero
      integer ram_index;
      initial
        for (ram_index = 0; ram_index < RAM_DEPTH; ram_index = ram_index + 1)
          BlockRAM[ram_index] = {RAM_WIDTH{1'b0}};
    end
  endgenerate

  always @(posedge clock) begin //Lectura y escritura de la RAM
    if (Write_enable)
      
      BlockRAM[WriteAdress] <= Dato_input;

    if (Read_Enable)
      RAM_DATA <= BlockRAM[ReadAdress];
  end

  //  The following code generates HIGH_PERFORMANCE (use output register) or LOW_LATENCY (no output register)
  generate
    if (RAM_PERFORMANCE == "LOW_LATENCY") begin: no_output_register

      // The following is a 1 clock cycle read latency at the cost of a longer clock-to-out timing
       assign Dato_output = RAM_DATA;

    end else begin: output_register

      // The following is a 2 clock cycle read latency with improve clock-to-out timing

      reg [RAM_WIDTH-1:0] Dato_output_reg = {RAM_WIDTH{1'b0}};

      always @(posedge clock)
        if (rstb)
          Dato_output_reg <= {RAM_WIDTH{1'b0}};
        else if (regceb)
          Dato_output_reg <= RAM_DATA;

      assign Dato_output = RAM_DATA;

    end
  endgenerate
				
						
endmodule
