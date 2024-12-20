# This is the file where should insert your own code.
#
# Author: Your Name <your@email.com>

from collections import defaultdict
import pulp

##### Exercise 2.1 #####


def __convert_to_ilp(nodes, edges, relaxed=False):
    cat = pulp.LpBinary
    if relaxed:
        cat = pulp.LpContinuous
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
                cat=cat,
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
                cat=cat,
            )
            obj += var * cost
            lift_vars[(edge.left, label_left), (edge.right, label_right)] = var

    ilp.setObjective(obj)
    return ilp, (orig_vars, lift_vars)


# Sherali-Adams linearization
def convert_to_ilp(nodes, edges, relaxed=False):
    ilp, (orig_vars, lift_vars) = __convert_to_ilp(nodes, edges, relaxed)
    sums = defaultdict(lambda: defaultdict(lambda: pulp.LpAffineExpression()))
    # sums = (node, label) -> other_node -> expr
    for (left, right), var in lift_vars.items():
        sums[left][right[0]] += var
        sums[right][left[0]] += var
    for this, others in sums.items():
        for expr in others.values():
            ilp += orig_vars[this] == expr
    return ilp, (orig_vars,)


# Fortet linearization
def convert_to_ilp_fortet(nodes, edges, relaxed=False):
    ilp, (orig_vars, lift_vars) = __convert_to_ilp(nodes, edges, relaxed)
    for (left, right), var in lift_vars.items():
        left_var = orig_vars[left]
        right_var = orig_vars[right]
        ilp += var <= left_var
        ilp += var <= right_var
        ilp += var >= (left_var + right_var - 1)
    return ilp, (orig_vars,)


def ilp_to_labeling(nodes, edges, lp, args):
    vars = args[0]
    labeling = []
    for i, node in enumerate(nodes):
        max = 0
        argmax = None
        for label in range(len(node.costs)):
            cur = pulp.value(vars[i, label])
            if cur > max:
                max = cur
                argmax = label
        labeling.append(argmax)
    return labeling


##### Exercise 2.2 #####
# Relaxed Sherali-Adams linearization
def convert_to_lp(nodes, edges):
    return convert_to_ilp(nodes, edges, relaxed=True)


# Relaxed Fortet linearization
def convert_to_lp_fortet(nodes, edges):
    return convert_to_ilp_fortet(nodes, edges, relaxed=True)


def lp_to_labeling(nodes, edges, lp, args):
    return ilp_to_labeling(nodes, edges, lp, args)
