# -*- coding: utf-8 -*-
from db_mysql_connector.Connection_sql import *

__author__ = 'luisangel'

chilean_cities_cache = []


def setup_chilean_cities_cache(connection):
    query = 'SELECT city_name, country_code, region_code, latitude, longitude ' \
            'FROM cities where country_code="cl" and selected=1;'
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        if data is None:
            global chilean_cities_cache
            chilean_cities_cache = []
        else:
            global chilean_cities_cache
            chilean_cities_cache = [{'city_name': x[0],
                                     'country_code': x[1],
                                     'region_code': x[2],
                                     'latitude': x[3],
                                     'longitude': x[4]} for x in data]
    except MySQLdb.Error:
        print "Error: unable to fetch data"
        sys.exit(1)


def get_city_by_name(gdb_sql, city_name):
    query = "select country_code, region_code, longitude, latitude " \
            "from geodict2.cities " \
            "where city_name = %s and country_code = 'cl' and selected=1;"
    try:
        cursor = gdb_sql.cursor()
        cursor.execute(query, (city_name,))
        data = cursor.fetchall()
        if data is None:
            return None
        else:
            return [{'country_code': x[0],
                     'region_code': x[1],
                     'latitude': x[2],
                     'longitude': x[3]}
                    for x in data]
    except MySQLdb.Error:
        print "Error: unable to fetch data"
        return -1
