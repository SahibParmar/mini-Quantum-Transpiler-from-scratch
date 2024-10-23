from qiskit import QuantumCircuit


class QuantumGate:
    '''Class for defining quantum different gates'''
    def __init__(self,operation,qubit_args,timestamp,Parameter=None):
        if operation not in ['H','T','CNOT','S','X','Y','Z','Rx','Ry','Rz','CZ','CCNOT','SWAP']:
            if operation[-1]=='+' and operation[:-1] not in ['H','T','CNOT','S','X','Y','Z','Rx','Ry','Rz','CZ','CCNOT','SWAP']:
                raise Exception(f'Unknown operation:-{operation}')
        self.operation=operation
        self.qubit_args=qubit_args
        self.Parameter=Parameter
        self.timestamp=timestamp
    def __str__(self):
        if self.Parameter!=None:
            return f'{self.operation}({self.qubit_args},{self.Parameter})'
        return f'{self.operation}({self.qubit_args})'




class Quantum_circuit:
    '''Class for defining a quantum circuit'''
    def __init__(self,num_qubits=1,num_bits=1):
        self.num_qubits=num_qubits
        self.num_bits=num_bits
        self.timestamp=0   # equivalent to number of total operations
        self.operations=[]
    def apply(self,operation,qubits,Parameter=None):
        for q in qubits:
            if q >= self.num_qubits:
                raise Exception(f'Qubit-{q} not exist in your system')
        self.timestamp+=1
        gate=QuantumGate(operation,qubits,self.timestamp,Parameter)
        self.operations.append(gate)

    def __str__(self):
        return f'{self.operations}'




if __name__=='__main__':
    circuit=Quantum_circuit(1,1)
    circuit.apply('H',[0])
    circuit.apply('H',[0])
    print(circuit)