# Author: Stefan Haller <stefan.haller@iwr.uni-heidelberg.de>

from tsukuba import *
import exercise_2 as student

for nodes, edges in all_models():
    prog, (orig_vars,) = student.convert_to_lp(nodes, edges)
    prog.solve()
