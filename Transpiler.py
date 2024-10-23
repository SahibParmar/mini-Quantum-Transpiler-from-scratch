from Quantum import Quantum_circuit,QuantumGate
from qiskit import *

class Partition:
    def __init__(self,member_Gate,id):
        self.members=[member_Gate]
        self.Partition_id=id
        self.applicable_timestamp=member_Gate.timestamp
    def __str__(self):
        temp=''
        for i in self.members: temp+=str(i)
        return temp
    def add_member(self,member):
        self.members.append(member)

def is_independent(gate,partition):
    query_qubits=set(gate.qubit_args)
    for operation in partition.members:
        if set(operation.qubit_args).intersection(query_qubits)!=set():
            return False
    return True

class Transpiler:


    def __init__(self,circuit):
        self.circuit=circuit
        self.qubit_timestamp={i:0 for i in range(circuit.num_qubits)}
        self.Partition_cnt=0

    def decompose_necessary_gates(self):
        operations=[]
        cnt=0
        for ind,gate in enumerate(self.circuit.operations):
            x=gate.qubit_args
            match gate.operation:
                case 'CCNOT':
                    # H3​⋅T3†​⋅CNOT2,3​⋅T3​⋅T2​⋅CNOT1,3​⋅T3†​⋅CNOT2,3​⋅T3​⋅T2​⋅H3
                    cnt+=1;operations.append(QuantumGate('H',[x[2]],cnt))
                    cnt+=1;operations.append(QuantumGate('T+',[x[2]],cnt))
                    cnt+=1;operations.append(QuantumGate('CNOT',[x[1],x[2]],cnt))
                    cnt+=1;operations.append(QuantumGate('T',[x[2]],cnt))
                    cnt+=1;operations.append(QuantumGate('T',[x[1]],cnt))
                    cnt+=1;operations.append(QuantumGate('CNOT',[x[0],x[2]],cnt))
                    cnt+=1;operations.append(QuantumGate('T+',[x[2]],cnt))
                    cnt+=1;operations.append(QuantumGate('CNOT',[x[1],x[2]],cnt))
                    cnt+=1;operations.append(QuantumGate('T',[x[2]],cnt))
                    cnt+=1;operations.append(QuantumGate('T',[x[1]],cnt))
                    cnt+=1;operations.append(QuantumGate('H',[x[2]],cnt))
                    continue
                case 'SWAP':
                    cnt+=1;operations.append(QuantumGate('CNOT',[x[0],x[1]],cnt))
                    cnt+=1;operations.append(QuantumGate('CNOT',[x[1],x[0]],cnt))
                    cnt+=1;operations.append(QuantumGate('CNOT',[x[0],x[1]],cnt))
                    continue
            cnt+=1
            operations.append(QuantumGate(gate.operation,gate.qubit_args,cnt,gate.Parameter))
        self.circuit.operations=operations

    def Create_Partitions(self):
        gates=self.circuit.operations

        self.Partition_cnt+=1
        I=[Partition(gates[0],self.Partition_cnt)]

        for q in gates[0].qubit_args:
            self.qubit_timestamp[q]=0
        for gate in gates[1:]:

            qubits=gate.qubit_args
            t=max([self.qubit_timestamp[q] for q in qubits])

            found=False
            ind=t
            for p in I[t:]:
                if len(p.members)<self.circuit.num_qubits and is_independent(gate,p):
                    I[ind].add_member(gate)
                    #update timestamps of each participant qubit
                    for q in qubits:
                        self.qubit_timestamp[q]=ind
                    found=True
                    break
                ind+=1
            if not found:
                self.Partition_cnt+=1
                I.append(Partition(gate,self.Partition_cnt))
                for q in gate.qubit_args:
                    self.qubit_timestamp[q]=len(I)-1

        return I

    def transpile(self,fusion=False,display_the_optimization=False):
        self.decompose_necessary_gates()
        if display_the_optimization:
           print('------------------------------------------------')
           print('\tCircuit before optimization')
           display_circuit(self.circuit)
        if fusion:
           self.circuit=fuse_gates(self.circuit)
        if display_the_optimization:
           print('------------------------------------------------')
           print('\tCircuit After fusion of gates')
           display_circuit(self.circuit)
        I=self.Create_Partitions()
        new_operations=[]
        depth=0
        for p in I:
            depth+=1
            for member in p.members:
                member.timestamp=depth
                new_operations.append(member)
        self.circuit.operations=new_operations
        if display_the_optimization:
           print('------------------------------------------------')
           print('\nAfter parallelization')
           display_circuit(self.circuit)
        return self.circuit
    




def display_circuit(circuit):
    '''Note: Please execute this function after transpiling the circuit to avoid errors!!'''
    qc = QuantumCircuit(circuit.num_qubits,circuit.num_bits)


# Handle error here: sometimes it is possible that user can provide parameter for hadamard gate ->
# handleException

    current_depth=1
    for gate in circuit.operations:
            operation=gate.operation
            qubits=gate.qubit_args
            Parameter=gate.Parameter
            timestamp=gate.timestamp
            if timestamp>current_depth:
                qc.barrier(label=f'depth-{current_depth}')
                # current_depth=timestamp
                current_depth+=1
            match operation:
                case 'H':
                    qc.h(qubits)
                case 'X':
                    qc.x(qubits)
                case 'T':
                    qc.t(qubits)
                case 'Y':
                    qc.y(qubits)
                case 'Z':
                    qc.z(qubits)
                case 'Rx':
                    # print(Parameter)
                    qc.rx(Parameter,qubits)
                case 'Ry':
                    qc.ry(Parameter,qubits)
                case 'Rz':
                    qc.rz(Parameter,qubits)
                case 'CZ':
                    qc.cz(qubits[0],qubits[1])
                case 'CNOT':
                    qc.cx(qubits[0],qubits[1])
                case 'T+':
                    qc.tdg(qubits)
                case 'S':
                    qc.s(qubits)



    qc.barrier(label=f'depth-{current_depth}')
    print(qc)







def is_fusable(gate1,gate2):
    if gate1.qubit_args!=gate2.qubit_args:
      return False

    if gate1.operation=='T' and gate2.operation=='T+' or gate1.operation=='T+' and gate2.operation=='T':
      return True
    elif gate1.operation==gate2.operation:
      return True

    return False
'''
T2=S (S gate).
T4=ZT4=Z (Z gate).
T6=S†T6=S† (Inverse of S gate).
The T gate completes a cycle after 8 powers: T8=IT8=I.

'''

def fuse(gate1,gate2):
    if gate1.operation=='Rx' or gate1.operation=='Ry' or gate1.operation=='Rz':
      if gate1.Parameter+gate2.Parameter==180:
        match gate1.operation:
          case 'Rx':
            print(2)
            return QuantumGate('X',gate1.qubit_args,gate1.timestamp)
          case 'Ry':
            print(3)
            return QuantumGate('Y',gate1.qubit_args,gate1.timestamp)
          case 'Rz':
            print(4)
            return QuantumGate('Z',gate1.qubit_args,gate1.applicable_timestamp)
      if gate1.Parameter+gate2.Parameter==90 and gate1.operation=='Rz':
          return QuantumGate('S',gate1.qubit_args,gate1.timestamp)


      return QuantumGate(gate1.operation,gate1.qubit_args,gate1.timestamp,Parameter=gate1.Parameter+gate2.Parameter)

    if gate1.operation=='T' and gate2.operation=='T':
      return QuantumGate('S',gate1.qubit_args,gate1.timestamp)
    if gate1.operation=='S' and gate2.operation=='S':
      return QuantumGate('Z',gate1.qubit_args,gate1.timestamp)

    else:
        # now returning identity
        return None



# gate fusion algorithm
def fuse_gates(circuit):
    operations=circuit.operations
    new_operations=[]
    current_depth=1
    qubit_wise_operations={i:[] for i in range(circuit.num_qubits)}
    for gate in operations:
        for q in gate.qubit_args:
            qubit_wise_operations[q].append(gate)

    for qubit in qubit_wise_operations:
      new_operations=[]
      skip_next_gate=False

      for ind,gate in enumerate(qubit_wise_operations[qubit]):
        if skip_next_gate==True:
          skip_next_gate=False
          continue
        if ind==len(qubit_wise_operations[qubit])-1:
            if len(gate.qubit_args)>1:
             if qubit==min(gate.qubit_args):
              new_operations.append(gate)
            else:
              new_operations.append(gate)
            break
        gate1=gate;gate2=qubit_wise_operations[qubit][ind+1]
        if is_fusable(gate1,gate2):
          fused_gate=fuse(gate1,gate2)
          if fused_gate!=None:
            new_operations.append(fused_gate)
          skip_next_gate=True
        else:
          # avoiding applying multi qubit gate multiple times
          if len(gate1.qubit_args)>1:
            if qubit==min(gate1.qubit_args):
              new_operations.append(gate1)
          else:
              new_operations.append(gate1)
      qubit_wise_operations[qubit]=new_operations
    merged_operations=[]
    for qubit in qubit_wise_operations:
      merged_operations+=qubit_wise_operations[qubit]
    merged_operations.sort(key=lambda x:x.timestamp)
    circuit.operations=merged_operations

    return circuit







