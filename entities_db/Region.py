import MySQLdb

__author__ = 'luisangel'


def get_id_region_by_name(name_region, connection):
    query = "SELECT idRegion FROM Region where name=%s;"
    try:
        cursor = connection.cursor()
        cursor.execute(query, (name_region,))
        data = cursor.fetchone()
        if data is None:
            return None
        else:
            return data[0]
    except MySQLdb.Error:
        print "Error: unable to fetch data"
        return -1
