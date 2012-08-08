import psycopg2

psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)

DB_CONFIG = {
    "database": "musicbrainz_db",
    "user": "musicbrainz",
    "password": "musicbrainz"
}

class MusicBrainz():
    def __enter__(self):
        self._conn = psycopg2.connect(**DB_CONFIG)
        return self

    def __exit__(self, type, value, traceback):
        self._conn.close()
    
    def get_labels(self):
        keys = ("id", "mbid", "name")
        query = """
            SELECT label.id, label.gid, label_name.name
            FROM label, label_name
            WHERE label.name = label_name.id"""
        curr = self._conn.cursor()
        curr.execute(query)
        labels = (dict(zip(keys, l)) for l in curr.fetchall())
        curr.close()
        return labels

    def get_relations(self):
        keys = ("rel_type", "label_id0", "label_id1")
        query = """
            SELECT link_type.name, l_l_l.entity0, l_l_l.entity1
            FROM l_label_label AS l_l_l, link, link_type 
            WHERE l_l_l.link = link.id 
                AND link.link_type = link_type.id"""
        curr = self._conn.cursor()
        curr.execute(query)
        relations = (dict(zip(keys, r)) for r in curr.fetchall())
        curr.close()
        return relations
