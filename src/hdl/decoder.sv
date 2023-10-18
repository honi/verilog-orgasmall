`include "config.sv"

module decoder (
    input [`INST_SIZE-1:0] inst,
    output logic [`OPCODE_BITS-1:0] opcode,
    output logic [`REGISTER_BITS-1:0] rx,
    output logic [`REGISTER_BITS-1:0] ry,
    output logic [`IMM_BITS-1:0] imm
);

localparam integer OPCODE_START = `INST_SIZE - 1;
localparam integer OPCODE_END = OPCODE_START - `OPCODE_BITS + 1;
localparam integer RX_START = OPCODE_END - 1;
localparam integer RX_END = RX_START - `REGISTER_BITS + 1;
localparam integer RY_START = RX_END - 1;
localparam integer RY_END = RY_START - `REGISTER_BITS + 1;
localparam integer IMM_START = `INST_SIZE - 8;
localparam integer IMM_END = 0;

assign opcode = inst[OPCODE_START:OPCODE_END];
assign rx = inst[RX_START:RX_END];
assign ry = inst[RY_START:RY_END];
assign imm = inst[IMM_START:IMM_END];

`ifdef COCOTB_SIM
initial begin
    $dumpfile("decoder.vcd");
    $dumpvars(0, decoder);
end
`endif

endmodule
