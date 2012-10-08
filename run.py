#!/usr/bin/env python

"""
This file is part of RIAAPath.

RIAAPath is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

RIAAPath is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with RIAAPath.  If not, see <http://www.gnu.org/licenses/>.
"""

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
    print(tree)

    if not os.path.isdir("dist"):
        os.mkdir("dist")

    with open("dist/riaalabels.js", "w") as output:
        output.write(json.dumps(tree))
