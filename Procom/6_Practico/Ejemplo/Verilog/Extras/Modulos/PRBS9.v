//MOdulo PRBS Q e I
module prbsQI (
    input  clock,
    input  i_reset,
    input  i_enable, 
    output o_PRBSI,
    output o_PRBSQ
);
    
reg [8:0] ShiftRegPRBSI  = 9'b110101010; //Semillas 
reg [8:0] ShiftRegPRBSQ  = 9'b111111110; 

reg [8:0] ShiftRegPRBSIAux; //registros auxiliares
reg [8:0] ShiftRegPRBSQAux;

reg outPRBSI;
reg outPRBSQ;

    always @(posedge clock) begin
        if (i_reset) begin
            ShiftRegPRBSI  <= 9'b110101010;
            ShiftRegPRBSQ  <= 9'b111111110;
            ShiftRegPRBSIAux <= ShiftRegPRBSI;  
            ShiftRegPRBSQAux <= ShiftRegPRBSQ;   
        end
        else if(i_enable == 1'b1) begin
            ShiftRegPRBSIAux <= ShiftRegPRBSI; // --> Aux 
            ShiftRegPRBSQAux <= ShiftRegPRBSQ; // --> Aux

            ShiftRegPRBSI    <= {ShiftRegPRBSI[7:0],ShiftRegPRBSI[8]}; // --> Roto
            ShiftRegPRBSQ    <= {ShiftRegPRBSQ[7:0],ShiftRegPRBSQ[8]}; // --> Roto

            ShiftRegPRBSI[0] <= ShiftRegPRBSIAux[4]^ShiftRegPRBSIAux[8]; // --> hago xor
            ShiftRegPRBSQ[0] <= ShiftRegPRBSQAux[4]^ShiftRegPRBSQAux[8]; // --> hago xor

            outPRBSI <= ShiftRegPRBSI[8]; // --> obtengo la salida
            outPRBSQ <= ShiftRegPRBSQ[8]; // --> obtengo la salida
        end
        else begin
            ShiftRegPRBSI <= ShiftRegPRBSI;
            ShiftRegPRBSQ <= ShiftRegPRBSQ; 
        end
    end
    
assign o_PRBSI = outPRBSI;  //salida de las PRBS Q e I
assign o_PRBSQ = outPRBSQ;

endmodule   