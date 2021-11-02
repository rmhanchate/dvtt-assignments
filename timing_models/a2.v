module comb_delay(in_a, in_b, in_c, out);

	input	in_a, in_b, in_c;
	output	out;
	wire fan_1, fan_2, fan_3, fan_4, fan_5;

	and	#(2, 3) gat1 (fan_1, in_a, in_b);
	or	#(2, 3) gat2 (fan_2, in_b, in_c);
	nand	#(2, 1) gat3 (fan_3, fan_1, fan_2);
	nor	#(2, 1) gat4 (fan_4, fan_1, in_a);
	or	#(2, 3) gat5 (fan_5, fan_3, in_c);
	and	#(2, 3) gat6 (out, fan_4, fan_5);

endmodule
