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

import psycopg2

DB_CONFIG = {
    "database": "musicbrainz_db",
    "user": "musicbrainz",
    "password": "musicbrainz"
}


class MusicBrainz():
    def __init__(self):
        psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
        self._conn = psycopg2.connect(**DB_CONFIG)

    def disconnect(self):
        self._conn.close()

    def _query_db(self, fields, query):
        curr = self._conn.cursor()
        curr.execute(query)
        results = (dict(zip(fields, r)) for r in curr.fetchall())
        curr.close()
        return results

    def get_labels(self):
        fields = ("id", "mbid", "name", "country")
        query = """
            SELECT label.id, label.gid, label_name.name, country.iso_code
                FROM label LEFT OUTER JOIN country ON
                        label.country = country.id,
                     label_name
                WHERE label.name = label_name.id;
            """
        return self._query_db(fields, query)

    def get_relations(self):
        fields = ("rel_type", "label_id0", "label_id1")
        query = """
            SELECT link_type.name, l_l_l.entity0, l_l_l.entity1
            FROM l_label_label AS l_l_l, link, link_type
            WHERE l_l_l.link = link.id
                AND link.link_type = link_type.id"""
        return self._query_db(fields, query)
