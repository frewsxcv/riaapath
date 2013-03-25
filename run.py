#!/usr/bin/env python

import json
import sys
import os

from lib.mbz import mbz_conn
from lib.graph import Graph


if __name__ == "__main__":
    graph = Graph()

    with mbz_conn() as mbz:
        graph.add_labels(mbz.labels)
        graph.add_relations(mbz.relations)

    tree = graph.generate_riaa_tree()

    if not os.path.isdir("dist"):
        os.mkdir("dist")

    with open("dist/riaalabels.js", "w") as output:
        output.write(json.dumps(tree))
