module a_tb;
	
	reg	in_a, in_b, in_c;
	wire	out;
	comb_delay dut (in_a, in_b, in_c, out);

	initial begin
		$dumpfile("a.vcd");
		$dumpvars(0, a_tb);
	end

	initial repeat(100) begin
		#10;
		in_a = {$random} % 2;
		in_b = {$random} % 2;
		in_c = {$random} % 2;
	end
	
endmodule
