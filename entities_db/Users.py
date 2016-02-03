import os
import json
from geodict.geodict_lib import *

__author__ = 'luisangel'

REGIONS = {'03': 'antofagasta',
           '05': 'atacama',
           '07': 'coquimbo',
           '14': 'puerto montt',
           '11': 'maule',
           '02': 'aysen',
           '16': 'arica',
           '04': 'temuco',
           '17': 'valdivia',
           '10': 'magallanes',
           '15': 'tarapaca',
           '01': 'valparaiso',
           '06': 'concepcion',
           '08': 'rancagua',
           '12': 'santiago'
           }

REGIONS_INV = {'Antofagasta': '03',
               'Atacama': '05',
               'Coquimbo': '07',
               'Los Lagos': '14',
               'Maule': '11',
               'Aysen': '02',
               'Arica y Parinacota': '16',
               'Araucania': '04',
               'Los Rios': '17',
               'Magallanes': '10',
               'Tarapaca': '15',
               'Valparaiso': '01',
               'Biobio': '06',
               'O\'Higgins': '08',
               'RM Santiago': '12'
               }


def get_user_location_sql(connection, id_user):
    query = "SELECT * FROM User_location WHERE idUser = %s;"
    try:
        cursor = connection.cursor()
        cursor.execute(query, (id_user,))
        data = cursor.fetchall()
        if data is None:
            return []
        else:
            return [[x[0], x[1], x[2], x[3], x[4]] for x in data]
    except MySQLdb.Error:
        print "Error: unable to fetch data"
        sys.exit(1)


def get_id_user_sql(connection, id_user):
    query = "SELECT idUser FROM Users_table WHERE idUser = %s;"
    try:
        cursor = connection.cursor()
        cursor.execute(query, (id_user,))
        data = cursor.fetchall()
        if data is None:
            return []
        else:
            return [x[0] for x in data]
    except MySQLdb.Error:
        print "Error: unable to fetch data"
        sys.exit(1)


def get_user_sql(gdb_sql, id_user):
    query = "select * " \
            "from Users_table " \
            "where idUser = %s ;"
    try:
        cursor = gdb_sql.cursor()
        cursor.execute(query, (id_user,))
        data = cursor.fetchall()
        if data is None:
            return []
        else:
            return [{
                        'id': x[0],
                        'screen_name': x[1],
                        'time_zone': x[2],
                        'name': x[3],
                        'followers_count': x[4],
                        'geo_enabled': x[5],
                        'description': x[6],
                        'tweet_chile': x[7],
                        'location': x[8],
                        'friends_count': x[9],
                        'verified': x[10],
                        'entities': x[11],
                        'utc_offset': x[12],
                        'statuses_count': x[13],
                        'lang': x[14],
                        'url': x[15],
                        'created_at': x[16],
                        'listed_count': x[17]
                    }
                    for x in data]
    except MySQLdb.Error:
        print "Error: unable to fetch data"
        return -1


def get_id_lost_users_sql(connection):
    query = "SELECT idLostUser FROM LostUser;"
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        if data is None:
            return []
        else:
            return [x[0] for x in data]
    except MySQLdb.Error:
        print "Error: unable to fetch data"
        return -1


def get_user_json(path, id_user):
    user_file_name = os.path.join(path, str(id_user) + '.json')
    user = {}
    if os.path.exists(user_file_name):
        user = json.loads(file(user_file_name).read())
    return user


def create_user_json(user={}, user_file_name=str()):
    with open(user_file_name, 'w') as outf:
        outf.write(json.dumps(user, indent=1))
        print("UserJson id: " + str(user['id']) + " create.")


def insert_lost_user(connection, id_user):
    try:
        x = connection.cursor()
        x.execute('INSERT INTO LostUser VALUES (%s) ', (
            id_user,))
        connection.commit()
    except MySQLdb.DatabaseError, e:
        print 'Error %s' % e
        connection.rollback()


def insert_user_sql(connection, user):
    try:
        x = connection.cursor()
        x.execute('INSERT INTO Users_table VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ',
                  (user['id'],
                   user['screen_name'],
                   user['time_zone'],
                   user['name'],
                   user['followers_count'],
                   user['geo_enabled'],
                   user['description'],
                   user['tweet_chile'],
                   user['location'],
                   user['friends_count'],
                   user['verified'],
                   user['entities'],
                   user['utc_offset'],
                   user['statuses_count'],
                   user['lang'],
                   user['url'],
                   user['created_at'],
                   user['listed_count'],
                   user['seed']))
        connection.commit()
    except MySQLdb.DatabaseError, e:
        print 'Error %s' % e
        connection.rollback()
        return

    if user['chile'] is False:
        return

    try:
        x = connection.cursor()
        x.execute('INSERT INTO User_location VALUES (%s,%s,%s,%s,%s) ', (user['id'],
                                                                         user['country_code'],
                                                                         user['region_code'],
                                                                         user['longitude'],
                                                                         user['latitude']
                                                                         ))
        connection.commit()
    except MySQLdb.DatabaseError, e:
        print 'Error %s' % e
        connection.rollback()
        return


def set_seed_user(gdb_sql, id_user):
    try:
        x = gdb_sql.cursor()
        x.execute('UPDATE Users_table SET seed = 1 WHERE idUser=%s ;',
                  (id_user,))
        gdb_sql.commit()
    except MySQLdb.DatabaseError, e:
        print 'Error {0:s}'.format(e)
        gdb_sql.rollback()
