# This is the file where should insert your own code.
#
# Author: Your Name <your@email.com>

from collections import defaultdict
import pulp

##### Exercise 2.1 #####


def __convert_to_ilp(nodes, edges):
    ilp = pulp.LpProblem("GM")
    obj = pulp.LpAffineExpression()
    orig_vars = {}
    for i, node in enumerate(nodes):
        total = pulp.LpAffineExpression()
        for label, cost in enumerate(node.costs):
            var = pulp.LpVariable(
                "node:%d;label:%d" % (i, label),
                lowBound=0,
                upBound=1,
                cat=pulp.LpBinary,
            )
            obj += var * cost
            total += var
            orig_vars[(i, label)] = var
        ilp += total == 1

    lift_vars = {}
    for i, edge in enumerate(edges):
        for (label_left, label_right), cost in edge.costs.items():
            var = pulp.LpVariable(
                "edge:%d,%d;labels:%d,%d"
                % (edge.left, edge.right, label_left, label_right),
                lowBound=0,
                upBound=1,
                cat=pulp.LpBinary,
            )
            obj += var * cost
            left = orig_vars[edge.left, label_left]
            right = orig_vars[edge.right, label_right]
            lift_vars[left, right] = var

    ilp.setObjective(obj)
    return ilp, (orig_vars, lift_vars)


# Sherali-Adams linearization
def convert_to_ilp(nodes, edges):
    ilp, (orig_vars, lift_vars) = __convert_to_ilp(nodes, edges)
    sums = defaultdict(lambda: pulp.LpAffineExpression())
    for (left, right), var in lift_vars.items():
        sums[left] += var
        # sums[right] += var
    for lhs, rhs in sums.items():
        ilp += lhs == rhs
    return ilp, (orig_vars,)


# Fortet linearization
def convert_to_ilp_fortet(nodes, edges):
    ilp, (orig_vars, lift_vars) = __convert_to_ilp(nodes, edges)
    for (left, right), var in lift_vars.items():
        ilp += var <= left
        ilp += var <= right
        ilp += var >= (left + right - 1)
    return ilp, (orig_vars,)


def ilp_to_labeling(nodes, edges, lp, args):
    vars = args[0]
    labeling = []
    for i, node in enumerate(nodes):
        for label in range(len(node.costs)):
            if pulp.value(vars[i, label]) == 1:
                labeling.append(label)
                break
    return labeling


##### Exercise 2.2 #####
# Relaxed Sherali-Adams linearization
def convert_to_lp(nodes, edges):
    lp = pulp.LpProblem("GM")
    # populate LP
    return lp


# Relaxed Fortet linearization
def convert_to_lp_fortet(nodes, edges):
    lp = pulp.LpProblem("GM")
    # populate LP
    return lp


def lp_to_labeling(nodes, edges, lp):
    labeling = []
    # compute labeling
    return labeling
