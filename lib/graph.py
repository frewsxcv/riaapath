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

import networkx as nx

from riaa import riaa_labels
from copy import copy


class Graph():
    def __init__(self):
        self.db = nx.MultiDiGraph()
        self.rel_rules = {
            "label ownership": (1, 0, "owned_by"),
            "label reissue": (1, 0, "catalog_reissued_by"),
            "label rename": (0, 1, "renamed_to"),
            "label distribution": (1, 0, "catalog_distributed_by"),
            "business association": (0, 1, "business_association_with")
        }

    def add_labels(self, labels):
        for label in labels:
            label_mbid = label["mbid"]
            label_id = label["id"]
            attrs = {"name": label["name"], "mbid": label_mbid}
            if label["country"]:
                attrs["country"] = label["country"]
            if label_mbid in riaa_labels:
                attrs["riaa"] = riaa_labels[label_mbid]
            self.db.add_node(label_id, attrs)

    def add_relations(self, relations):
        """
        """
        for relation in relations:
            self.add_relation(relation)

    def add_relation(self, relation):
        labels = (relation["label_id0"], relation["label_id1"])
        rel_type = relation["rel_type"]
        rel_rule = self.rel_rules[rel_type]
        self.db.add_edge(labels[rel_rule[0]], labels[rel_rule[1]],
                attr_dict={"rel": rel_rule[2]})

    def generate_riaa_tree(self):
        tree = {}
        for label_id in self.db:
            path = self.get_riaa_path(label_id)
            if len(path) > 0:
                label_mbid = self.db.node[label_id]["mbid"]
                if len(path) == 1:
                    parent_label_id = path[0]
                    parent_label = self.db.node[parent_label_id]
                else:
                    parent_label_id = path[1]
                    parent_label = self.db.node[parent_label_id]
                    rel = self.db.edge[label_id][parent_label_id][0]["rel"]
                    parent_label["rel"] = rel
                parent_label["parent"] = parent_label["mbid"]
                tree[label_mbid] = parent_label
        return tree

    def get_riaa_path(self, label_id):
        shortest = []
        paths = nx.single_source_shortest_path(self.db, label_id)
        for path in paths.values():
            if self.is_riaa(path[-1]):
                if len(shortest) == 0:
                    shortest = path
                elif len(path) < len(shortest):
                    shortest = path
        return shortest

    def is_riaa(self, label_id):
        """
        Determine if the label is RIAA affiliated
        label_id
        """
        return "riaa" in self.db.node[label_id]
 
    def get_riaa_path_old(self, label_id, visited=None):
        if not visited:
            visited = set()
        if "riaa" in self.db.node[label_id]:
            return [label_id]
        paths = []
        for parent_label_id in self.db.successors(label_id):
            if parent_label_id not in visited:
                visited.add(parent_label_id)
                path = self.get_riaa_path(parent_label_id, copy(visited))
                if len(path) > 0:
                    path.insert(0, label_id)
                    paths.append(path)
        return min(paths) if len(paths) > 0 else []
