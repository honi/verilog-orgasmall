`include "../../shared/hdl/config.sv"

`include "../../alu/hdl/alu.sv"
`include "../../decoder/hdl/decoder.sv"
`include "../../memory/hdl/memory.sv"
`include "../../registers/hdl/registers.sv"

module cpu (
    input rst,
    input clk
);

// Program counter.
reg [`ADDR_SIZE-1:0] pc;

// Instrucción decodificada.
wire [`INST_SIZE-1:0] inst;
wire [`OPCODE_BITS-1:0] opcode;
wire [`REGISTER_BITS-1:0] idx_rx;
wire [`REGISTER_BITS-1:0] idx_ry;

// Cables para interconectar los componentes.
wire [`WORD_SIZE-1:0] data_rx;
wire [`WORD_SIZE-1:0] data_ry;
wire [`WORD_SIZE-1:0] data_imm;
wire [`WORD_SIZE-1:0] data_alu_out;
reg [`WORD_SIZE-1:0] registers_data_in;
reg [`WORD_SIZE-1:0] data_memory_data_in;
reg [`ADDR_SIZE-1:0] data_memory_addr;
reg registers_en_write;
reg data_memory_en_write;

memory #(
    .WORD_SIZE(`INST_SIZE),
    .ADDR_SIZE(`ADDR_SIZE)
) inst_memory (
    .data_in(0),
    .data_out(inst),
    .addr(pc),
    .en_write(1'b0), // never write
    .rst(1'b0),
    .clk(clk)
);

decoder decoder (
    .inst_hi(inst[`INST_SIZE-1:`WORD_SIZE]),
    .inst_lo(inst[`WORD_SIZE-1:0]),
    .opcode(opcode),
    .rx(idx_rx),
    .ry(idx_ry),
    .imm(data_imm)
);

registers #(
    .WORD_SIZE(`WORD_SIZE),
    .COUNT(`NUM_REGISTERS)
) registers (
    .data_in(registers_data_in),
    .idx_write(idx_rx), // Todas las ops guardan en rx.
    .en_write(registers_en_write),
    .data_out_a(data_rx),
    .data_out_b(data_ry),
    .idx_out_a(idx_rx),
    .idx_out_b(idx_ry),
    .rst(rst),
    .clk(clk)
);

alu #(
    .WORD_SIZE(`WORD_SIZE)
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

// Activamos las señales de control y ruteamos los datos según la instrucción.
always_comb begin
    registers_en_write = 0;
    data_memory_en_write = 0;

    case (opcode)
        // ALU ops
        ADD, ADC, SUB, AND, OR, XOR, CMP, MOV, INC, DEC, SHR, SHL: begin
            registers_en_write = 1;
            registers_data_in = data_alu_out;
        end

        // Jumps
        JMP, JC, JZ, JN: begin
        end

        // Load/Store ops
        SET: begin
            registers_en_write = 1;
            registers_data_in = data_imm;
        end
        STR, LOAD, RSTR, RLOAD: begin
        end
    endcase
end

`ifdef COCOTB_SIM
initial begin
    $dumpfile("dump.vcd");
    $dumpvars(0, cpu);
end
`endif

endmodule
