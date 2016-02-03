from twitter.api3 import *
from entities_db.Users import *
from Geolocation.User_location import *

__author__ = 'luisangel'

FOLLOWERS_OF_FOLLOWERS_LIMIT = 3000000

SEED = "Emol"
BD_JSON = "../../twitter-users"

enc = lambda x: x.encode('ascii', errors='ignore')

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


def get_user(gdb, id_user):
    # USE SQL
    results = get_user_sql(gdb, id_user)
    if len(results) >= 1:
        u = results[0]
        u['chile'] = True if len(get_user_location_sql(gdb, id_user)) > 0 else False
        if u['chile'] is False:
            return u
    # USE JSON
    user_file_name = os.path.join(BD_JSON, str(id_user) + '.json')

    if os.path.exists(user_file_name):
        user = json.loads(file(user_file_name).read())
        return user
    # USE API TWITTER
    u = get_user_twitter(id_user)

    if u is None:
        return None

    if u.protected is True:
        return None

    user = {'id': id_user}

    try:
        user['screen_name'] = unicode(u.screen_name).encode('utf-8') if u.screen_name is not None else ''
    except AttributeError:
        user['screen_name'] = ''

    try:
        user['time_zone'] = unicode(u.time_zone).encode('utf-8') if u.time_zone is not None else ''
    except AttributeError:
        user['time_zone'] = ''

    try:
        user['name'] = unicode(u.name).encode('utf-8') if u.name is not None else ''
    except AttributeError:
        user['name'] = ''

    user['followers_count'] = u.followers_count

    user['geo_enabled'] = u.geo_enabled

    try:
        user['description'] = unicode(u.description).encode('utf-8') if u.description is not None else ''
    except AttributeError:
        user['description'] = ''

    user['tweet_chile'] = 0

    try:
        user['location'] = unicode(u.location).encode('utf-8') if u.location is not None else ''
    except AttributeError:
        user['location'] = ''

    user['friends_count'] = u.friends_count

    user['verified'] = u.verified

    try:
        user['entities'] = unicode(u.entities).encode('utf-8') if u.entities is not None else ''
    except AttributeError:
        user['entities'] = ''

    try:
        user['utc_offset'] = unicode(u.utc_offset).encode('utf-8') if u.utc_offset is not None else ''
    except AttributeError:
        user['utc_offset'] = ''

    user['statuses_count'] = u.statuses_count

    try:
        user['lang'] = unicode(u.lang).encode('utf-8') if u.lang is not None else ''
    except AttributeError:
        user['lang'] = ''

    try:
        user['url'] = unicode(u.url).encode('utf-8') if u.url is not None else ''
    except AttributeError:
        user['url'] = ''

    user['created_at'] = str(u.created_at)

    user['listed_count'] = u.listed_count

    user['seed'] = 1 if user['screen_name'] == SEED else 0

    user = is_location(gdb, user, chilean_cities_cache)

    if user['chile'] is True:
        create_user_json(user, user_file_name)

    insert_user_sql(gdb, user)

    return user


def get_follower_ids(gdb, centre):

    try:

        user = get_user(gdb, centre)
        if user is None or user['chile'] is False:
            return "Seed not found"
        print 'user id %s' % str(centre)

        ids_loser = get_id_lost_users_sql(gdb)
        set_id_loser = set(ids_loser)
        set_follower_id = set(user['followers_ids'])
        follower_ids = list(set_follower_id - set_id_loser)
        print str(len(follower_ids))
        try:
            start = int(sys.argv[1])
        except IndexError:
            start = 0
        for fid in follower_ids[start:int(FOLLOWERS_OF_FOLLOWERS_LIMIT)]:
            print "Processing: " + str(start) + ' Fid = ' + str(fid)
            start += 1
            get_user(gdb, fid)
    except Exception, error:
        print 'Error: '
        print error
        return "Error in code"

    return "Finish run"


def main():
    screen_name = SEED

    matches = api.lookup_users(screen_names=[screen_name])

    if len(matches) == 1:
        gdb = get_connection_sql()
        setup_chilean_cities_cache(gdb)
        print get_follower_ids(gdb, matches[0].id)
    else:
        print 'Sorry, could not find the Twitter user with screen name: %s' % screen_name


def test():
    gdb = get_connection_sql()
    us = get_user_location_sql(gdb, 67645047)
    gdb.close()
    print str(us)
    pass


if __name__ == "__main__":
    main()
