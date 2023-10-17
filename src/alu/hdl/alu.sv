`timescale 1us/1us

typedef enum {
  ADD,
  SUB,
  LEFT_SHIFT,
  RIGHT_SHIFT_ARITHMETIC,
  RIGHT_SHIFT_LOGIC,
  AND,
  OR,
  XOR,
  EQUAL
} opcode;

module alu #(
    parameter longint WORD_SIZE = 16
)(
    input [WORD_SIZE-1:0] a,
    input [WORD_SIZE-1:0] b,
    output logic [WORD_SIZE-1:0] out, // TODO: reg o logic?
    input opcode op
);

always_comb begin
    case (op)
        ADD: out = a + b;
        SUB: out = a - b;
        LEFT_SHIFT: out = a << b;
        RIGHT_SHIFT_ARITHMETIC: out = a >> b; // TODO
        RIGHT_SHIFT_LOGIC: out = a >> b;
        AND: out = a & b;
        OR: out = a | b;
        XOR: out = a ^ b;
        EQUAL: out = (a == b) ? 1'b1 : 1'b0;
        default: out = '0;
    endcase
end

`ifdef COCOTB_SIM
initial begin
    $dumpfile("dump.vcd");
    $dumpvars(0, alu);
end
`endif

endmodule
