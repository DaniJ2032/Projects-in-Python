//Ejemplo de shiftreg
module PRBS (
    input clk,
    input i_reset,
    output o_PRBSI
);
    
reg [8:0] ShiftRegPRBSI  = 9'b110101010; 
reg [8:0] ShiftRegPRBSIAux;          
reg outPRBSI;


// reg aux;
    always @(posedge clk) begin
        if (~i_reset) begin
            ShiftRegPRBSI  <= 9'b110101010;
            ShiftRegPRBSIAux <= ShiftRegPRBSI;    
        end
        else begin
            ShiftRegPRBSIAux <= ShiftRegPRBSI; // --> Aux 
            ShiftRegPRBSI    <= {ShiftRegPRBSI[7:0],ShiftRegPRBSI[8]}; // --> Roto
            ShiftRegPRBSI[0] <= ShiftRegPRBSIAux[4]^ShiftRegPRBSIAux[8]; // --> hago xor
            outPRBSI <= ShiftRegPRBSI[8]; // --> obtengo la salida
        end
    end
assign o_PRBSI = outPRBSI;

endmodule
