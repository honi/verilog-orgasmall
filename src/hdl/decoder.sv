`include "config.sv"

module decoder (
    input [`WORD_SIZE-1:0] inst_hi,
    input [`WORD_SIZE-1:0] inst_lo,
    output logic [`OPCODE_BITS-1:0] opcode,
    output logic [`REGISTER_BITS-1:0] rx,
    output logic [`REGISTER_BITS-1:0] ry,
    output logic [`IMM_BITS-1:0] imm
);

always_comb begin
    opcode = inst_hi >> (`WORD_SIZE - `OPCODE_BITS);
    rx = inst_hi & ((1 << `REGISTER_BITS) - 1);
    ry = inst_lo >> (`WORD_SIZE - `REGISTER_BITS);
    imm = inst_lo;
end

`ifdef COCOTB_SIM
initial begin
    $dumpfile("decoder.vcd");
    $dumpvars(0, decoder);
end
`endif

endmodule
