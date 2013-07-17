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
      
//Asynchronous Logic
assign reset = ~rst;

//Synchronous Logic
always @(posedge clk) begin
  if (reset) begin
    led               <= 2'b11;
    throb_counter     <= 26'd0;
  end
  else begin
    led[1]            <= 1;
    if (button[0]) begin
      led[0]          <= 1;
    end
    if (button[1]) begin
      led[1]          <= 1;
    end

    if (throb_counter >= 32'h0100_0000) begin
      throb_counter <= 26'd0;
      led[0]        <= !led[0]; 
    end else begin
      throb_counter <= throb_counter + 26'd1;
    end
  end
end

endmodule
