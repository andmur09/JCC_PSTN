# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 16:06:07 2021

@author: kpb20194
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 13:37:11 2021

@author: kpb20194
"""

from numpy.lib.twodim_base import _trilu_indices_form_dispatcher
from make_instances import makeSTN
import sys
from PSTN_class import PSTN
import pickle as pkl
import numpy as np
import logging
import re
inf = 10000

def main():
    # logging.basicConfig(filename='elevators_generation.log', level=logging.INFO)
    directory = "pstns/domains/tfd-benchmarks/woodworking-numeric/"
    no_instances = 30
    names, instances, deadlines = makeSTN(directory, no_instances)

    if len(names) != len(instances) or len(names) != len(deadlines):
        raise ValueError("Number of instances/names/deadlines not equal")

    # Makes instances of PSTN class using set of timepoints and set of constraints.
    woodworking = []
    for i in range(no_instances):
        name = names[i]
        timepoints = instances[i][0]
        constraints = instances[i][1]
        woodworking.append(PSTN(name, timepoints, constraints))

    for i in range(len(deadlines)):
        if deadlines[i] != None:
            deadlines[i] = deadlines[i]

    # For each PSTN, finds the start and last timePoint in the network and thus the constraint bounding the overall plan duration, creates additional instances of
    # each PSTN with varying deadlines.
    woodworking_ud = []
    for i in range(len(woodworking)):
        problem = woodworking[i]
        deadline = deadlines[i]
        if deadline != None:
            problem.addDeadline(deadline)
            woodworking_ud.append(problem)
    

    # Changes below actions to be probabilistic in PSTN
    for instance in woodworking_ud:
        print([constraint.intervals["ub"] for constraint in instance.constraints])
        constraints = instance.constraints
        for constraint in constraints:
            if "do-spray-varnish_start" in constraint.source.description and "do-spray-varnish_end" in constraint.sink.description:
                if re.search("\(.+\)", constraint.source.description).group() == re.search("\(.+\)", constraint.sink.description).group():
                    constraint.setType("pstc")
                    mean = (constraint.intervals["lb"] + constraint.intervals["ub"])/2
                    constraint.distribution = {"type": "gaussian", "mean": mean, "variance": 0.2 * mean}
                    constraint.intervals = {"lb": 0, "ub": inf, "value": 1}
            elif "do-glaze_start" in constraint.source.description and "do-glaze_end" in constraint.sink.description:
                if re.search("\(.+\)", constraint.source.description).group() == re.search("\(.+\)", constraint.sink.description).group():
                    constraint.setType("pstc")
                    mean = (constraint.intervals["lb"] + constraint.intervals["ub"])/2
                    constraint.distribution = {"type": "gaussian", "mean": mean, "variance": 0.2 * mean}
                    constraint.intervals = {"lb": 0, "ub": inf, "value": 1}
            elif "do-grind_start" in constraint.source.description and "do_grind_end" in constraint.sink.description:
                if re.search("\(.+\)", constraint.source.description).group() == re.search("\(.+\)", constraint.sink.description).group():
                    constraint.setType("pstc")
                    mean = (constraint.intervals["lb"] + constraint.intervals["ub"])/2
                    constraint.distribution = {"type": "gaussian", "mean": mean, "variance": 0.2 * mean}
                    constraint.intervals = {"lb": 0, "ub": inf, "value": 1}
            elif "do-plane_start" in constraint.source.description and "do-plane_end" in constraint.sink.description:
                if re.search("\(.+\)", constraint.source.description).group() == re.search("\(.+\)", constraint.sink.description).group():
                    constraint.setType("pstc")
                    mean = (constraint.intervals["lb"] + constraint.intervals["ub"])/2
                    constraint.distribution = {"type": "gaussian", "mean": mean, "variance": 0.2 * mean}
                    constraint.intervals = {"lb": 0, "ub": inf, "value": 1}
            elif "do-saw_start" in constraint.source.description and "do-saw_end" in constraint.sink.description:
                if re.search("\(.+\)", constraint.source.description).group() == re.search("\(.+\)", constraint.sink.description).group():
                    constraint.setType("pstc")
                    mean = (constraint.intervals["lb"] + constraint.intervals["ub"])/2
                    constraint.distribution = {"type": "gaussian", "mean": mean, "variance": 0.2 * mean}
                    constraint.intervals = {"lb": 0, "ub": inf, "value": 1}

    for i in range(len(woodworking_ud)):
        with open("pstns/problems/woodworking/{}".format(woodworking_ud[i].name), "wb") as f:
            pkl.dump(woodworking_ud[i], f)

if __name__ == "__main__":
    main()