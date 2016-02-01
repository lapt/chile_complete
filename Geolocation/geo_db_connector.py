import MySQLdb
import credentials as k
import sys

Q_RANDLATLON_REGION = "SELECT latitude,longitude FROM cities where country_code = %s AND region_code = %s ORDER BY RAND() LIMIT 1;"

Q_RANDLATLON_COUNTRY = "SELECT latitude,longitude FROM cities where country_code = %s ORDER BY RAND() LIMIT 1;"

Q_LATLON_COUNTRY = "SELECT latitude,longitude FROM countries where country_code = %s;"


def execute(connection, q_script):
    """
	executes a mysql script
	"""
    try:
        cursor = connection.cursor()
        cursor.execute(q_script)
    except MySQLdb.Error:
        print "Error: unable to execute"
        return -1


def getClosestCity_ori(connection, latitude, longitude, radio):
    """
	Returns the closest city, region code and country code
	"""
    try:
        cursor = connection.cursor()
        cursor.execute("call closestcity(%s,%s,%s);", (latitude, longitude, radio,))
        data = cursor.fetchone()
        return data
    except MySQLdb.Error:
        print "Error: unable to fetch data"
        return -1


def getClosestCity(connection, latitude, longitude, radio):
    query = ''' SELECT country_code
				FROM (
					SELECT city_name, country_code, latitude, longitude, r,
	       					111.045 
	       					* DEGREES(ACOS(COS(RADIANS(latpoint))
	                 		* COS(RADIANS(latitude))
	                 		* COS(RADIANS(longpoint) - RADIANS(longitude))
	                 		+ SIN(RADIANS(latpoint))
	                 		* SIN(RADIANS(latitude)))) AS distance_in_km
	 				FROM cities
	 				JOIN (
	        			SELECT  %s  AS latpoint,  %s AS longpoint, %s AS r 
	   					) AS p
	 				WHERE latitude
	   					BETWEEN latpoint  - (r / 111.045)
	       				AND latpoint  + (r / 111.045)
	   				AND longitude
	   					BETWEEN longpoint - (r / (111.045 * COS(RADIANS(latpoint))))
	       				AND longpoint + (r / (111.045 * COS(RADIANS(latpoint))))
  				) d
 				WHERE distance_in_km <= r
 				ORDER BY distance_in_km
 				LIMIT 1 
 			'''
    try:
        cursor = connection.cursor()
        cursor.execute(query, (latitude, longitude, radio,))
        data = cursor.fetchone()
        if data is None:
            return None
        else:
            return data[0]
    except MySQLdb.Error:
        print "Error: unable to fetch data"
        return -1


def getClosestCityAdmins(connection, latitude, longitude, radio):
    query = ''' SELECT country_code, region_code
  				FROM (
					SELECT city_name, country_code, region_code, latitude, longitude, r,
       					111.045 
       					* DEGREES(ACOS(COS(RADIANS(latpoint))
                 		* COS(RADIANS(latitude))
                 		* COS(RADIANS(longpoint) - RADIANS(longitude))
                 		+ SIN(RADIANS(latpoint))
                 		* SIN(RADIANS(latitude)))) AS distance_in_km
 					FROM cities
 					JOIN (
        				SELECT  %s  AS latpoint,  %s AS longpoint, %s AS r 
   					) AS p
 					WHERE latitude
   						BETWEEN latpoint  - (r / 111.045)
       					AND latpoint  + (r / 111.045)
   					AND longitude
   						BETWEEN longpoint - (r / (111.045 * COS(RADIANS(latpoint))))
       					AND longpoint + (r / (111.045 * COS(RADIANS(latpoint))))
  				) d
 				WHERE distance_in_km <= r
 				ORDER BY distance_in_km
 				LIMIT 1
 			'''
    try:
        cursor = connection.cursor()
        cursor.execute(query, (latitude, longitude, radio,))
        data = cursor.fetchone()
        if data is None:
            return None
        else:
            return data
    except MySQLdb.Error:
        print "Error: unable to fetch data"
        return -1


def getLatitudeLongitudeFromCountryCode(connection, country_code):
    """
	Returns the latitude and longitude from a country givens its code
	"""
    try:
        cursor = connection.cursor()
        cursor.execute(Q_LATLON_COUNTRY, (country_code))
        data = cursor.fetchone()
        return data
    except MySQLdb.Error:
        print "Error: unable to fetch data"
        return -1


def randomLatitudeLongitudeForRegion(connection, country_code, admin1_code):
    """
	Returns the lat and lon for a random city in the country and region 
	given as parameters
	"""
    try:
        cursor = connection.cursor()
        if admin1_code == '00':
            cursor.execute(Q_RANDLATLON_COUNTRY, (country_code))
        else:
            cursor.execute(Q_RANDLATLON_REGION, (country_code, admin1_code))
        data = cursor.fetchone()
        return data
    except MySQLdb.Error:
        print "Error: unable to fetch data"
        return -1

# if __name__ == "__main__":
#	main()
