# for storing old code

from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister

control_qubits = QuantumRegister(14, name="c")
target_qubit = QuantumRegister(1, name='t')
ancilla_qubits = QuantumRegister(5, name='a')
classical_bits = ClassicalRegister(1, name='out')

#### design 1 - 192 depth
# Design 1: (3-4-3) 
# b0-13, t, a0-4
# 4 3-bit in place control gates (b0-11)->(a0-3)
# 1 4-bit in place control gate taking 2 remaining bits and 2 auxiliary bits (b12-13, a0-1) -> a4
# 3 3-bit in place control gate that takes (a2-4) -> t
qc = QuantumCircuit(control_qubits, target_qubit, ancilla_qubits, classical_bits)
for i in range(14):
    qc.x(control_qubits[i])

for i in range(4):
    qc.mcx(control_qubits[3*i:3*(i+1)], ancilla_qubits[i])

qc.mcx(control_qubits[12:14] + ancilla_qubits[0:2], ancilla_qubits[4])
qc.mcx(ancilla_qubits[2:5], target_qubit[0])

qc.mcx(control_qubits[12:14] + ancilla_qubits[0:2], ancilla_qubits[4])
for i in range(4):
    qc.mcx(control_qubits[3*i:3*(i+1)], ancilla_qubits[i])
qc.measure(target_qubit[0], classical_bits[0])
qc.draw()
####

#### design 2 - 151 depth
qc = QuantumCircuit(control_qubits, target_qubit, ancilla_qubits, classical_bits)
for i in range(14):
    qc.x(control_qubits[i])

for i in range(3):
    qc.mcx(control_qubits[3*i:3*(i+1)], ancilla_qubits[i])
# 0 - 8
qc.mcx(control_qubits[9:13], ancilla_qubits[3])

qc.mcx(ancilla_qubits[0:2] + control_qubits[13:14], ancilla_qubits[4])

qc.mcx(ancilla_qubits[2:5], target_qubit[0])

# uncompute
qc.mcx(ancilla_qubits[0:2] + control_qubits[13:14], ancilla_qubits[4])
for i in range(3):
    qc.mcx(control_qubits[3*i:3*(i+1)], ancilla_qubits[i])
# 0 - 8
qc.mcx(control_qubits[9:13], ancilla_qubits[3])

qc.measure(target_qubit[0], classical_bits[0])

qc.draw()
####

#### design 3
qc = QuantumCircuit(control_qubits, target_qubit, ancilla_qubits, classical_bits)
for i in range(14):
    qc.x(control_qubits[i])

for i in range(7):
    qc.mcx(control_qubits[2*i:2*(i+1)], ancilla_qubits[i], mode='recursion')
for i in range(8):
    qc.mcx(control_qubits[2*i:2*(i+1)], ancilla_qubits[i], mode='recursion')
# 0 - 11
qc.mcx(control_qubits[12:14] + [ancilla_qubits[0]], ancilla_qubits[4], mode='recursion')
qc.mcx(ancilla_qubits[1:5], target_qubit[0], mode='recursion')
qc.measure(target_qubit[0], classical_bits[0])
qc.draw()
####