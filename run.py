#!/usr/bin/python3

# Load the main quantum circuit representing game logic (constant)
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer, transpile # pip3 install qiskit
gameCircuit = QuantumCircuit.from_qasm_file("game.qasm")

# Load the mapping of states to outputs (constant)
import json, gzip
outputData = json.loads(gzip.GzipFile("outputs.json.gz", 'r').read().decode("utf-8"))

# Start in the default state 
state = "0000000000000010011011"

simulator = Aer.get_backend('qasm_simulator')

# Game loop
while True:

    # Display the state
    try:
        print(outputData[state])
    except:
        print(outputData["error"])

    # Get the user's input
    classicalInput = input("              Command (try \"help\"): ")

    # Generate circuit combining user input and prev game state
    inputCircuit = QuantumCircuit(QuantumRegister(3, "inpt"), QuantumRegister(2, "plhp"), QuantumRegister(2, "enhp"), QuantumRegister(4, "evnt"), QuantumRegister(3, "item"), QuantumRegister(8, "ancl"), ClassicalRegister(22, "cout"))
    inputState = state[:-3] + {"h":"001","m":"011","a":"100","b":"101","f":"110","i":"111"}[classicalInput[0]]
    for i, char in enumerate(inputState[::-1]):
        if char == "1": inputCircuit.x(i)

    circuit = inputCircuit.compose(gameCircuit)
    compiled_circuit = transpile(circuit, simulator)
    # Combine and run the circuit (one shot)
    output = simulator.run(compiled_circuit, shots=1)
    state = list(output.result().get_counts().keys())[0][0:22]

