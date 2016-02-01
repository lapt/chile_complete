import MySQLdb
import sys
import credentials as k

__author__ = 'luisangel'


def get_connection_sql():
    # Returns a connection object whom will be given to any DB Query function.
    try:
        connection = MySQLdb.connect(host=k.GEODB_HOST, port=3306, user=k.GEODB_USER,
                                     passwd=k.GEODB_KEY, db=k.GEODB_NAME)
        return connection
    except MySQLdb.DatabaseError, e:
        print 'Error %s' % e
        sys.exit(1)


def close_connection_sql(connection):
    connection.close()


def execute(connection, q_script):
    # executes a mysql script
    try:
        cursor = connection.cursor()
        cursor.execute(q_script)
    except MySQLdb.Error:
        print "Error: unable to execute"
        return -1
