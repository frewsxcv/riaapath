from contextlib import contextmanager

import psycopg2


DB_CONFIG = {
    "database": "musicbrainz_db",
    "user": "musicbrainz",
    "password": "musicbrainz"
}


class Label():
    def __init__(self, id, mbid, name, country):
        self.id = id
        self.mbid = mbid
        self.name = name
        self.country = country


class LabelRelation():
    def __init__(self, type, id1, id2):
        self.type = type
        self.id1 = id1
        self.id2 = id2


@contextmanager
def mbz_conn():
    mbz = MusicBrainz()
    mbz.connect()
    yield mbz
    mbz.disconnect()


class MusicBrainz():
    def __init__(self):
        psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)

    def connect(self):
        self._conn = psycopg2.connect(**DB_CONFIG)

    def disconnect(self):
        self._conn.close()

    def _query(self, sql):
        curr = self._conn.cursor()
        curr.execute(sql)
        results = curr.fetchall()
        curr.close()
        return results

    @property
    def labels(self):
        sql = """
            SELECT label.id, label.gid, label_name.name, country.iso_code
                FROM label LEFT OUTER JOIN country ON
                        label.country = country.id,
                     label_name
                WHERE label.name = label_name.id;"""
        return [Label(*row) for row in self._query(sql)]

    @property
    def relations(self):
        sql = """
            SELECT link_type.name, l_l_l.entity0, l_l_l.entity1
            FROM l_label_label AS l_l_l, link, link_type
            WHERE l_l_l.link = link.id
                AND link.link_type = link_type.id"""
        return [LabelRelation(*row) for row in self._query(sql)]
