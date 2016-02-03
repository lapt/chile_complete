from twitter.api3 import *
from entities_db.Users import *
from Geolocation.User_location import *

__author__ = 'luisangel'

FOLLOWERS_OF_FOLLOWERS_LIMIT = 3000000
DEPTH = 1
SEED = "Emol"
BD_JSON = "../../twitter-users"
FID = 0
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
        user['screen_name'] = u.screen_name
    except AttributeError:
        user['screen_name'] = None
    user['screen_name'] = unicode(user['screen_name']).encode('utf-8') if user['screen_name'] is not None else ''

    try:
        user['time_zone'] = u.time_zone
    except AttributeError:
        user['time_zone'] = None
    user['time_zone'] = unicode(user['time_zone']).encode('utf-8') if user['time_zone'] is not None else ''

    try:
        user['name'] = u.name
    except AttributeError:
        user['name'] = None
    user['name'] = unicode(user['name']).encode('utf-8') if user['name'] is not None else ''

    user['followers_count'] = u.followers_count

    user['geo_enabled'] = u.geo_enabled

    try:
        user['description'] = u.description
    except AttributeError:
        user['description'] = None
    user['description'] = unicode(user['description']).encode('utf-8') if user['description'] is not None else ''

    user['tweet_chile'] = 0

    try:
        user['location'] = u.location
    except AttributeError:
        user['location'] = None
    user['location'] = unicode(user['location']).encode('utf-8') if user['location'] is not None else ''

    user['friends_count'] = u.friends_count

    user['verified'] = u.verified

    try:
        user['entities'] = u.entities
    except AttributeError:
        user['entities'] = None
    user['entities'] = unicode(user['entities']).encode('utf-8') if user['entities'] is not None else ''

    try:
        user['utc_offset'] = u.utc_offset
    except AttributeError:
        user['utc_offset'] = None
    user['utc_offset'] = unicode(user['utc_offset']).encode('utf-8') if user['utc_offset'] is not None else ''

    user['statuses_count'] = u.statuses_count

    try:
        user['lang'] = u.lang
    except AttributeError:
        user['lang'] = None
    user['lang'] = unicode(user['lang']).encode('utf-8') if user['lang'] is not None else ''

    try:
        user['url'] = u.url
    except AttributeError:
        user['url'] = None
    user['url'] = unicode(user['url']).encode('utf-8') if user['url'] is not None else ''

    user['created_at'] = str(u.created_at)

    user['listed_count'] = u.listed_count

    user['seed'] = 1 if user['screen_name'] == SEED else 0

    user['followers_ids'] = u.followers_ids()

    user = is_location(gdb, user, chilean_cities_cache)

    if user['chile'] is True:
        create_user_json(user, user_file_name)

    insert_user_sql(gdb, user)

    return user


def get_relation_by_id(gdb, id):
    query = "MATCH ()-[role:Follower]->() where role.id={id} return role"
    param = {'id': id}
    results = gdb.query(query, params=param, data_contents=True)
    return results.rows


def get_follower_ids(gdb, centre, max_depth=1, current_depth=0,
                     taboo_list=[]):  # AQUI DEBEMOS VERFICAR LA VALIDEZ DE PASAR GBD
    # print 'current depth: %d, max depth: %d' % (current_depth, max_depth)
    # print 'taboo list: ', ','.join([ str(i) for i in taboo_list ])
    if current_depth == max_depth:
        print 'out of depth'
        return taboo_list

    if centre in taboo_list:
        # we've been here before
        print 'Repeated ID: ' + str(centre)
        return taboo_list
    else:
        taboo_list.append(centre)

    try:

        user = get_user(gdb, centre)
        if user is None or user['chile'] is False:
            return taboo_list
        print 'user id %s' % str(centre)

        cd = current_depth

        ids_loser = get_id_lost_users_sql(gdb)
        set_id_loser = set(ids_loser)
        set_follower_id = set(user['followers_ids'])
        follower_ids = list(set_follower_id - set_id_loser)

        try:
            start = int(sys.argv[1])
        except IndexError:
            start = 0
        for fid in follower_ids[start:int(FOLLOWERS_OF_FOLLOWERS_LIMIT)]:
            print "Processing: " + str(start)
            start += 1
            if start == 12:
                print "aqui"
            global FID
            FID = fid
            user2 = get_user(gdb, fid)

            if user2 is None or user2['chile'] is False:
                continue

            if cd + 1 < max_depth:
                taboo_list = get_follower_ids(gdb, fid, max_depth=max_depth,
                                              current_depth=cd + 1, taboo_list=taboo_list)

        if cd + 1 < max_depth and len(follower_ids) > FOLLOWERS_OF_FOLLOWERS_LIMIT:
            print 'No todos los seguidores fueron recuperados para %d.' % centre

    except Exception, error:
        print 'Error al recuperar los seguidores de usuario id: ' + str(centre) + " fid = " + str(FID)
        print error
        return taboo_list
        sys.exit(1)

    return taboo_list


def main():
    screen_name = SEED
    depth = int(DEPTH)

    if depth < 1 or depth > 3:
        print 'Depth value %d is not valid. Valid range is 1-3.' % depth
        sys.exit('Invalid depth argument.')

    print 'Max Depth: %d' % depth

    matches = api.lookup_users(screen_names=[screen_name])

    if len(matches) == 1:
        gdb = get_connection_sql()
        setup_chilean_cities_cache(gdb)
        print len(get_follower_ids(gdb, matches[0].id, max_depth=depth))
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
