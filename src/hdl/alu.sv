`include "config.sv"

module alu #(
    parameter longint WORD_SIZE = `WORD_SIZE
)(
    input opcode_t opcode,
    input [WORD_SIZE-1:0] a,
    input [WORD_SIZE-1:0] b,
    output logic [WORD_SIZE-1:0] out, // TODO: reg o logic?
    output logic flag_c,
    output logic flag_z,
    output logic flag_n
);

always_comb begin
    case (opcode)
        ADD: {flag_c, out} = a + b;
        ADC: {flag_c, out} = a + b + flag_c;
        SUB: {flag_c, out} = a - b;
        AND: out = a & b;
        OR: out = a | b;
        XOR: out = a ^ b;
        CMP: out = a == b;
        INC: out = a + 1;
        DEC: out = a - 1;
        SHR: out = a >> b;
        SHL: out = a << b;
        default: begin
            out = 0;
            flag_c = 0;
        end
    endcase
    case (opcode)
        AND, OR, XOR, CMP, INC, DEC, SHR, SHL: flag_c = 0;
    endcase
    flag_z = out == 0;
    flag_n = out[WORD_SIZE-1] == 1;
end

`ifdef SIM_ALU
initial begin
    $dumpfile("dump.vcd");
    $dumpvars(0, alu);
end
`endif

endmodule
