`include "config.sv"

module alu #(
    parameter longint WORD_SIZE = `WORD_SIZE
)(
    input opcode_t opcode,
    input [WORD_SIZE-1:0] a,
    input [WORD_SIZE-1:0] b,
    input carry_in,
    output logic [WORD_SIZE-1:0] out, // TODO: reg o logic?
    output reg flag_c,
    output reg flag_z,
    output reg flag_n
);

initial begin
    out = 0;
    flag_c = 0;
    flag_z = 0;
    flag_n = 0;
end

always_comb begin
    case (opcode)
        ADD: {flag_c, out} = a + b;
        ADC: {flag_c, out} = a + b + carry_in;
        SUB: {flag_c, out} = a - b;
        AND: out = a & b;
        OR: out = a | b;
        XOR: out = a ^ b;
        CMP: out = a == b;
        INC: out = a + 1;
        DEC: out = a - 1;
        SHR: out = a >> b;
        SHL: out = a << b;
        default: out = 0;
    endcase
    case (opcode)
        ADD, ADC, SUB, AND, OR, XOR, CMP: begin
            flag_z = out == 0;
            flag_n = out[WORD_SIZE-1] == 1;
        end
    endcase
end

`ifdef SIM_ALU
initial begin
    $dumpfile("dump.vcd");
    $dumpvars(0, alu);
end
`endif

endmodule
