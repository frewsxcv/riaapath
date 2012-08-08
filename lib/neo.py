import shutil
import os

from neo4j import GraphDatabase
from riaa import riaa_labels


class Neo4j():
    def __enter__(self):
        if os.path.isdir("tmp"):
            shutil.rmtree("tmp")
        self._db = GraphDatabase("tmp")
        self._node_index = self._db.node.indexes.create("labels")
        self._nodes = []
        return self

    def __exit__(self, type, value, traceback):
        self._db.shutdown()
        shutil.rmtree("tmp")

    def add_labels(self, labels):
        riaa_mbids = riaa_labels.keys()
        with self._db.transaction:
            for label in labels:
                l_mbid = label["mbid"]
                node = self._db.node(mbid=l_mbid, name=label["name"])
                if l_mbid in riaa_mbids:
                    node["riaasource"] = riaa_labels[l_mbid]
                self._node_index["id"][label["id"]] = node
                self._nodes.append(node)

    def add_relations(self, relations):
        with self._db.transaction:
            for relation in relations:
                self._add_relation(relation)

    def _add_relation(self, relation):
        label0 = self._node_index["id"][relation["label_id0"]][0]
        label1 = self._node_index["id"][relation["label_id1"]][0]
        rel_type = relation["rel_type"]
        if rel_type == "label ownership":
            label1.owned_by(label0)
        elif rel_type == "label reissue":
            label1.catalog_reissued_by(label0)
        elif rel_type == "label rename":
            label0.renamed_to(label1)
        elif rel_type == "label distribution":
            label1.catalog_distributed_by(label0)
        elif rel_type == "business association":
            label1.business_association_with(label0)
        else:
            label0.unknown_relation_with(label1)

    def generate_riaa_tree(self):
        tree = {}
        # TODO: There must be a better way of getting all nodes
        for node in self._nodes:
            mbid = self._find_riaa_parent(node)
            if mbid:
                tree[node["mbid"]] = mbid
            del node
        return tree

    def _find_riaa_parent(self, start_node, explored=None):
        # TODO: This is depth first. It should be breadth first.
        # TODO: It's also ugly and ineffecient
        if start_node.hasProperty("riaasource"):
            return {
                "sourceUrl": start_node["mbid"],
                "name": start_node["name"]
            }
        if not explored:
            explored = []
        explored.append(start_node["mbid"])
        for rel in start_node.relationships.outgoing:
            start_node = rel.startNode
            end_node = rel.endNode
            if end_node["mbid"] not in explored and \
                    self._find_riaa_parent(end_node, explored):
                return {
                    "parentMbid": end_node["mbid"],
                    "name": start_node["name"],
                    "parentRel": rel.type.name()
                }
        return False
