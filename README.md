# **Introduction**
The Quantum Transpiler is a lightweight tool designed to 
optimize and transform quantum circuits by translating high-level quantum algorithms into efficient, 
low-level quantum gate operations. This project focuses on applying decomposition, parallelization, and gate fusion optimization techniques 
to minimize gate count and circuit depth while preserving the intended functionality of the quantum algorithm.

# **Transpilation Techniques**
**1. Decomposition**
Break complex gates like controlled-U and multi-qubit gates into elementary gates (T, H, CNOT, etc.).
Example:

Toffoli gate can be decomposed into 6 CNOTs and several single-qubit gates.

**2. Parallelization**
Independent gates that operate on different qubits can be executed in parallel to minimize circuit depth.
Parallelization identifies commutative operations and reorders them.
T-gates are costly in fault-tolerant quantum computing. The transpiler applies fusion rules to reduce the total count of T-gates by merging them where possible.

**3. Fusion Rules**
Fusion rules are mathematical identities that simplify gate sequences, especially when optimizing for error-prone gates like T-gates. The transpiler automatically applies these rules to minimize circuit complexity.

# **Demo images**
**1. Without any optimizations:**
![A](https://github.com/user-attachments/assets/2a5ae414-44b0-4b64-980b-5709161a1e58)
**2. After applying gate fusion:**
![B](https://github.com/user-attachments/assets/a6e0a7ba-0495-4e1e-8617-55878424d739)
**3. After Parallelizing circuit:**
![C](https://github.com/user-attachments/assets/8dee9f58-8e1f-4e66-af77-029f36ec43bc)


