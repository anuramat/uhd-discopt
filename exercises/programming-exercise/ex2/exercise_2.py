# This is the file where should insert your own code.
#
# Author: Your Name <your@email.com>

import pulp

##### Exercise 2.1 #####

# Sherali-Adams linearization
def convert_to_ilp(nodes, edges):
    ilp = pulp.LpProblem('GM')
    # populate ILP
    return ilp


# Fortet linearization
def convert_to_ilp_fortet(nodes, edges):
    ilp = pulp.LpProblem('GM')
    # populate ILP
    return ilp


def ilp_to_labeling(nodes, edges, ilp):
    labeling = []
    # compute labeling
    return labeling


##### Exercise 2.2 #####
# Relaxed Sherali-Adams linearization
def convert_to_lp(nodes, edges):
    lp = pulp.LpProblem('GM')
    # populate LP
    return lp


# Relaxed Fortet linearization
def convert_to_lp_fortet(nodes, edges):
    lp = pulp.LpProblem('GM')
    # populate LP
    return lp


def lp_to_labeling(nodes, edges, lp):
    labeling = []
    # compute labeling
    return labeling
