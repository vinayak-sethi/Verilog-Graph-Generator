module HalfAdder( A, B, Sum, Carry);

	input A, B;
	output Sum, Carry;

	xor xor_0 (Sum, A, B);
	and and_0 (Carry, A, B);

endmodule
