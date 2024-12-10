#!/usr/bin/env python3
# This is the file where should insert your own code.
#
# Author: Your Name <your@email.com>


# For exercise 1.1
def evaluate_energy(nodes, edges, assignment):
    return 0.0


# For exercise 1.2
def bruteforce(nodes, edges):
    assignment = [0] * len(nodes)
    # TODO: implement brute-force algorithm here...
    energy = evaluate_energy(nodes, edges, assignment)
    return (assignment, energy)

# For exercise 1.3
def dynamic_programming(nodes, edges):
    F, ptr = None, None
    return F, ptr

def backtrack(nodes, edges, F, ptr):
    assignment = [0] * len(nodes)
    return assignment