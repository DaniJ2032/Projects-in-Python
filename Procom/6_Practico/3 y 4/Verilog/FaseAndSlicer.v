/* Módulo Slicer obtenemos una muestra cada 4 ciclos de reloj. Dicha muestra se le extrae
   el signo para el módulo que lo procede (Contador de BER)*/
module FaseAndSlicerQI(
    input               clock     ,
    input               i_reset   ,
    input               i_enable  , 
    input  signed [7:0] i_firI    ,
    input  signed [7:0] i_firQ    ,    
    input               i_valid   ,
    input         [1:0] i_selector,

    output              output_slicerI,
    output              output_slicerQ     
    );

//variables enteras
integer   i; 

//Registros y cables para el Slicer I
reg       firauxI             ; //registro para uso de retardo de la salida del filtro   
reg [7:0] selector_faseI [3:0];
wire      sal_muxI;

//Registros y cables para el Slicer Q
reg       firauxQ             ; //registro para uso de retardo de la salida del filtro   
reg [7:0] selector_faseQ [3:0];
wire      sal_muxQ;


always @(posedge clock) begin
    if (i_reset) begin
      for (i=0; i<4; i = i+1)begin
          selector_faseI[i] <= 8'b00000000; //REVISAR CUALQUIER COSA
          selector_faseQ[i] <= 8'b00000000;  
       end   
      firauxI        <= 0;
      firauxQ        <= 0;

   end else if (i_enable) begin
   
      selector_faseI[3] <= i_firI           ;
      selector_faseI[2] <= selector_faseI[3];
      selector_faseI[1] <= selector_faseI[2];
      selector_faseI[0] <= selector_faseI[1];
      firauxI           <= sal_muxI         ;

      selector_faseQ[3] <= i_firQ           ;
      selector_faseQ[2] <= selector_faseQ[3];
      selector_faseQ[1] <= selector_faseQ[2];
      selector_faseQ[0] <= selector_faseQ[1];
      firauxQ           <= sal_muxQ         ;
   end
end
//Salida de mux para seleccion cualquiera de las 4 fases en el slicer I, y se toma el bit MSB del signo 
assign sal_muxI = (i_selector == 2'b00 && i_valid) ? selector_faseI[3][7]  : (i_selector == 2'b01 && i_valid) 
                                                   ? selector_faseI[2][7]  : (i_selector == 2'b10 && i_valid) 
                                                   ? selector_faseI[1][7]  :  selector_faseI[0][7]; 

//Salida de mux para seleccion cualquiera de las 4 fases en el slicer Q, y se toma el bit MSB del signo 
assign sal_muxQ = (i_selector == 2'b00 && i_valid) ? selector_faseQ[3][7]  : (i_selector == 2'b01 && i_valid) 
                                                   ? selector_faseQ[2][7]  : (i_selector == 2'b10 && i_valid) 
                                                   ? selector_faseQ[1][7]  :  selector_faseQ[0][7];

/*Salidas de los SLicer Q  e I*/
assign output_slicerI = firauxI;
assign output_slicerQ = firauxQ;

endmodule
