#!/usr/bin/env python

import json
import sys

from lib.mbz import MusicBrainz
from lib.neo import Neo4j

if sys.argv[-1] in ("-q", "--quiet"):
    def log(msg):
        pass
else:
    def log(msg):
        sys.stdout.write(msg + "\n")

log("Connecting to MusicBrainz database")
with MusicBrainz() as mbz:
    log("Retrieving labels from MusicBrainz database")
    labels = mbz.get_labels()
    log("Retrieving label relationships from MusicBrainz database")
    relations = mbz.get_relations()
    log("Disconnecting from MusicBrainz database")

log("Creating temporary Neo4j database")
with Neo4j() as neo4j:
    log("Adding labels to Neo4j database")
    neo4j.add_labels(labels)
    log("Adding label relationships to Neo4j database")
    neo4j.add_relations(relations)
    log("Generating tree from populated Neo4j database")
    tree = neo4j.generate_riaa_tree()
    log("Disconnecting and removing temporary Neo4j database")

with open("riaalabels.json", "w") as output:
    log("Saving generated tree to riaalabels.json")
    output.write(json.dumps(tree))
