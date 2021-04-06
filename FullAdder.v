module FullAdder(A, B, Cin, Sum, Cout);

    input A, B, Cin;
    output Sum, Cout;
   	wire w1,w2,w3,w4,w5;
	
	xor xor_0 (w1, A, B);
	xor xor_1 (Sum, w1, Cin);
	
	and and_0 (w2, A, B);
	and and_1 (w3, A, Cin);
	and and_2 (w4, B, Cin);
	
	or or_0 (w5, w2, w3);
	or or_1 (Cout, w4, w5);

endmodule
