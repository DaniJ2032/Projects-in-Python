//////////////////////////////////////////////////////////////////////////////////
// AUTOR: Jose gomez Lazarte, Juarez Daniel 
// AÑO:   2023  
// NOMBRE: Módulo PRBS Q e I, proporciona datos aletarorios para los filtros  
//
//////////////////////////////////////////////////////////////////////////////////

module prbsQI (
    input  clock,
    input  i_reset,
    input  i_enable, 
    input  i_valid,
    output o_PrbsI, 
    output o_PrbsQ
);
    
reg [8:0] ShiftRegPRBSI; //Semillas 
reg [8:0] ShiftRegPRBSQ;   

    always @(posedge clock) begin
        if (i_reset) begin
            ShiftRegPRBSI  <= 9'b010101011;
            ShiftRegPRBSQ  <= 9'b111111110;
        end

        else if(i_enable && i_valid) begin

            ShiftRegPRBSI    <= {ShiftRegPRBSI[7:0],(ShiftRegPRBSI[4]^ShiftRegPRBSI[8])}; // --> Roto y aplico xor
            ShiftRegPRBSQ    <= {ShiftRegPRBSQ[7:0],(ShiftRegPRBSQ[4]^ShiftRegPRBSQ[8])}; // --> Roto y aplico xor
        end
        else begin
            ShiftRegPRBSI <= ShiftRegPRBSI;
            ShiftRegPRBSQ <= ShiftRegPRBSQ; 

        end
    end
    
assign o_PrbsI = ShiftRegPRBSI[8];  //salida de las PRBS Q e I
assign o_PrbsQ = ShiftRegPRBSQ[8];


endmodule 