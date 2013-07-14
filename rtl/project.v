// very minimal example top-level module

module main (
    output reg [1:0] led,
    input wire clk,
    input wire [1:0] button, // this is active low
    input wire rst

    );

    wire reset;
    assign reset = ~rst;

    reg [25:0] throb_counter = 0;

    always @(posedge clk) begin
        if (reset) begin
            led <= 2'b11;
            throb_counter <= 26'd0;
        end else begin
            led[0] <= (button[0] | button[1]);
            if (throb_counter >= 26'd50_000_000) begin
                led[1] <= !led[1]; 
                throb_counter <= 26'd0;
            end else begin
                throb_counter <= throb_counter + 26'd1;
            end
        end
    end

endmodule
