from neo4jrestclient.client import GraphDatabase
from neo4jrestclient import exceptions

__author__ = 'luisangel'


def get_connection_neo():
    gdb = GraphDatabase("http://neo4j:123456@localhost:7474/db/data/")
    return gdb


def set_chile_user(gdb, id_user, screen_name):
    with gdb.transaction(for_query=True) as tx:
        try:
            query = "MATCH(n) where n.id={id} set n+={region:'Chile', screen_name: {sn}} " \
                    "set n.chile=true remove n:Extranjero set n:Chile;"
            param = {'id': id_user, 'sn': screen_name}
            gdb.query(query, params=param)
        except exceptions.StatusException as e:
            print "Error in update user: " + e.result
            tx.rorollback()
            return


def get_user_node_by_id(gdb, id):
    query = "MATCH (n:User)WHERE n.id={id} RETURN n LIMIT 25"
    param = {'id': id}
    results = gdb.query(query, params=param, data_contents=True)
    if results.rows is not None:
        return results.rows[0][0]
    return None


def get_user_seed(gdb):
    query = "MATCH (n:Semilla) RETURN n"
    results = gdb.query(query, data_contents=True)
    return results.rows
