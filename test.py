
from Geolocation.User_location import *

__author__ = 'luisangel'

chilean_cities_cache = []


def setup_chilean_cities_cache(connection):
    query = 'SELECT city_name, country_code, region_code, latitude, longitude ' \
            'FROM cities where country_code="cl" and selected=1;'
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        global chilean_cities_cache
        if data is None:
            chilean_cities_cache = []
        else:
            chilean_cities_cache = [{'city_name': x[0],
                                     'country_code': x[1],
                                     'region_code': x[2],
                                     'latitude': x[3],
                                     'longitude': x[4]} for x in data]
    except MySQLdb.Error:
        print "Error: unable to fetch data"
        sys.exit(1)


def main():
    cn = getConnection()
    setup_chilean_cities_cache(cn)
    data = {'location': 'santiasco'}
    data = is_location(data, chilean_cities_cache)
    print data
if __name__ == '__main__':
    main()