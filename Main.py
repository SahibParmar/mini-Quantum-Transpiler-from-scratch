from Transpiler import *
from Quantum import Quantum_circuit,QuantumGate



circuit=Quantum_circuit(4,4)
circuit.apply('CCNOT',[0,1,2])
circuit.apply('T',[1])
circuit.apply('S',[1])
circuit.apply('H',[2])
circuit.apply('H',[0])
circuit.apply('Rx',[0],90)
circuit.apply('Rx',[0],90)


# circuit=fuse_gates(circuit)

compiler=Transpiler(circuit)
circuit=compiler.transpile(fusion=True,display_the_optimization=True)


