`include "config.sv"

module registers #(
    parameter longint WORD_SIZE = `WORD_SIZE,
    parameter longint COUNT = `NUM_REGISTERS,
    localparam longint COUNT_BITS = $clog2(COUNT)
)(
    input [WORD_SIZE-1:0] data_in,
    input [COUNT_BITS-1:0] idx_write,
    input en_write,

    output [WORD_SIZE-1:0] data_out_a,
    output [WORD_SIZE-1:0] data_out_b,
    input [COUNT_BITS-1:0] idx_out_a,
    input [COUNT_BITS-1:0] idx_out_b,

    input rst,
    input clk
);

reg [WORD_SIZE-1:0] data [0:COUNT-1];

longint i;

always_ff @ (posedge clk or posedge rst) begin
    if (rst) begin
        for (i = 0; i < COUNT; i = i + 1) begin
            data[i] <= '0;
        end
    end else begin
        if (en_write) data[idx_write] <= data_in;
    end
end

assign data_out_a = data[idx_out_a];
assign data_out_b = data[idx_out_b];

`ifdef SIM_REGISTERS
initial begin
    $dumpfile("dump.vcd");
    $dumpvars(0, registers);
end
// genvar k;
// for (k = 0; k < COUNT; k = k + 1) initial $dumpvars(0, data[k]);
`endif

endmodule
