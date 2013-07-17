// very minimal example top-level module

module main (

input               clk,
input               rst,

output  reg [1:0]   led,
input       [1:0]   button // this is active low
);

//Registers/Wires
wire reset;

reg   [31:0]  throb_counter = 0;
reg   [31:0]  throb_counter_x = 0;
      
reg   [15:0]  ar;
reg   [15:0]  ai;
reg   [15:0]  br;
reg   [15:0]  bi;
wire  [32:0]  pr;
wire  [32:0]  pi;


//Submodules
complex_multiplier cm (
  .clk (clk),     // input  clk
  .ar  (ar ),     // input  [15 : 0] ar
  .ai  (ai ),     // input  [15 : 0] ai
  .br  (br ),     // input  [15 : 0] br
  .bi  (bi ),     // input  [15 : 0] bi
  .pr  (pr ),     // output [32 : 0] pr
  .pi  (pi )      // output [32 : 0] pi
); 

//Asynchronous Logic
assign reset = ~rst;

//Synchronous Logic
always @(posedge clk) begin
  if (reset) begin
    led               <= 2'b11;
    throb_counter     <= 26'd0;
    throb_counter_x   <= 0;
    ar                <= 400;
    ai                <= 100;
    br                <= 200;
    bi                <= 1000;
  end
  else begin
    if (button[0]) begin
      throb_counter   <= 0;
      led[0]          <= 1;
      ar              <=  ar + 1;
      bi              <=  bi + 1;
    end

    if (button[1]) begin
      throb_counter_x <= 0;
      led[1]          <= 1;
      ai              <=  ai + 1;
      br              <=  br + 1;
    end

    if (throb_counter >= pr[31:0]) begin
      led[0]        <= !led[0]; 
      throb_counter <= 26'd0;
    end else begin
      throb_counter <= throb_counter + 26'd1;
    end

    if (throb_counter_x == pi[31:0]) begin
      led[0]        <= !led[0]; 
      throb_counter_x <= pi[31:0] + 1;
    end else begin
      throb_counter_x <= throb_counter + 26'd1;
    end
  end
end

endmodule
