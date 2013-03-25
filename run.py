#!/usr/bin/env python

import json
import sys
import os

from lib.mbz import MusicBrainz
from lib.graph import Graph


if __name__ == "__main__":
    mbz = MusicBrainz()
    labels = mbz.get_labels()
    relations = mbz.get_relations()
    mbz.disconnect()

    graph = Graph()
    graph.add_labels(labels)
    graph.add_relations(relations)
    tree = graph.generate_riaa_tree()

    if not os.path.isdir("dist"):
        os.mkdir("dist")

    with open("dist/riaalabels.js", "w") as output:
        output.write(json.dumps(tree))
