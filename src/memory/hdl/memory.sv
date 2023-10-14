`timescale 1us/1us

module memory (data_in, data_out, addr, we, oe, rst, clk);

// TODO: Tipos usados para los parámetros limitan las opciones de configuración?
parameter longint WORD_SIZE = 16;
parameter longint ADDR_SIZE = 16;
localparam longint MAX_ADDR = (1 << ADDR_SIZE) - 1;

input [WORD_SIZE-1:0] data_in;
output [WORD_SIZE-1:0] data_out;

input [ADDR_SIZE-1:0] addr;

input we; // write enable
input oe; // output enable
input rst;
input clk;

reg [WORD_SIZE-1:0] ram [0:MAX_ADDR];

longint i;

always_ff @ (posedge clk or posedge rst) begin
    if (rst) begin
        for (i = 0; i < MAX_ADDR; i = i + 1) begin
            ram[i] <= '0; // {(WORD_SIZE){1'b0}}
        end
    end else begin
        if (we) ram[addr] <= data_in;
    end
end

assign data_out = (oe & !we) ? ram[addr] : 'z; // {(WORD_SIZE){1'bz}}

`ifdef COCOTB_SIM
initial begin
    $display("WORD_SIZE = %0d bits", WORD_SIZE);
    $display("ADDR_SIZE = %0d bits", ADDR_SIZE);
    $display("MAX_ADDR = 0x%0h", MAX_ADDR);
    $dumpfile("dump.vcd");
    $dumpvars(0, memory);
end
`endif

endmodule
