`include "config.sv"

module alu #(
    parameter longint WORD_SIZE = `WORD_SIZE
)(
    input [WORD_SIZE-1:0] a,
    input [WORD_SIZE-1:0] b,
    output logic [WORD_SIZE-1:0] out, // TODO: reg o logic?
    input opcode_t opcode
);

always_comb begin
    case (opcode)
        ADD: out = a + b;
        ADC: out = a + b;
        SUB: out = a - b;
        AND: out = a & b;
        OR: out = a | b;
        XOR: out = a ^ b;
        CMP: out = (a == b) ? 1'b1 : 1'b0;
        INC: out = a + 1;
        DEC: out = a - 1;
        SHR: out = a >> b;
        SHL: out = a << b;
        default: out = '0;
    endcase
end

`ifdef SIM_ALU
initial begin
    $dumpfile("dump.vcd");
    $dumpvars(0, alu);
end
`endif

endmodule
