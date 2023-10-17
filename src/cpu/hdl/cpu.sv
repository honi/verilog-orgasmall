`include "../../shared/hdl/config.sv"

`include "../../alu/hdl/alu.sv"
`include "../../decoder/hdl/decoder.sv"
`include "../../memory/hdl/memory.sv"
`include "../../registers/hdl/registers.sv"

module cpu #(
    parameter longint WORD_SIZE = 8,
    parameter longint ADDR_SIZE = 8
)(
    input rst,
    input clk
);

reg [ADDR_SIZE-1:0] pc;
wire [(WORD_SIZE*2)-1:0] inst;
wire [`OPCODE_BITS-1:0] opcode;
wire [`REGISTER_BITS-1:0] idx_rx;
wire [`REGISTER_BITS-1:0] idx_ry;
wire [`WORD_SIZE-1:0] data_rx;
wire [`WORD_SIZE-1:0] data_ry;
wire [`WORD_SIZE-1:0] data_imm;
wire [`WORD_SIZE-1:0] data_alu_out;

memory #(
    .WORD_SIZE(WORD_SIZE * 2),
    .ADDR_SIZE(ADDR_SIZE)
) inst_memory (
    .data_in(0),
    .data_out(inst),
    .addr(pc),
    .en_write(1'b0), // never write
    .rst(1'b0),
    .clk(clk)
);

decoder decoder (
    .inst_hi(inst[(WORD_SIZE*2)-1:WORD_SIZE]),
    .inst_lo(inst[WORD_SIZE-1:0]),
    .opcode(opcode),
    .rx(idx_rx),
    .ry(idx_ry),
    .imm(data_imm)
);

registers #(
    .WORD_SIZE(WORD_SIZE),
    .COUNT(8)
) registers (
    .data_in(data_alu_out), // hardcoded
    .idx_write(idx_rx),     // hardcoded
    .en_write(1'b1),        // hardcoded
    .data_out_a(data_rx),
    .data_out_b(data_ry),
    .idx_out_a(idx_rx),
    .idx_out_b(idx_ry),
    .rst(rst),
    .clk(clk)
);

alu #(
    .WORD_SIZE(WORD_SIZE)
) alu (
    .a(data_rx),
    .b(data_ry),
    .out(data_alu_out),
    .opcode(opcode)
);

// TODO: Qué tipo de always habría que usar acá?
// TODO: Frenar la ejecución si opcode inválido.
always @ (posedge clk or posedge rst) begin
    if (rst) begin
        pc = 0;
    end else begin
        pc = pc + 1;
    end
end

`ifdef COCOTB_SIM
initial begin
    $dumpfile("dump.vcd");
    $dumpvars(0, cpu);
end
`endif

endmodule
