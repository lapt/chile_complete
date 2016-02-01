from query_neo4j.tools_neo import *
from db_mysql_connector.Connection_sql import *
from entities_db.Users import *

__author__ = 'luisangel'


def main():
    cn_neo = get_connection_neo()
    cn_sql = get_connection_sql()
    seeds = get_user_seed(cn_neo)
    for seed in seeds:
        id_user = int(seed[0]['id'])
        set_seed_user(cn_sql, id_user)
        print "Proceed id: " + str(id_user)
    pass


if __name__ == '__main__':
    main()
