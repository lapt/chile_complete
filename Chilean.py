from twitter.api1 import *
from entities_db.Users import *
from Geolocation.User_location import *

__author__ = 'luisangel'

FOLLOWERS_OF_FOLLOWERS_LIMIT = 3000000
DEPTH = 2
SEMILLA = "TerraChile"  # "soyarica"
BDJSON = "../../twitter-users"
ID_BAD = 0
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


def get_ids_by_seed(gdb, seed):  # Ids por semilla
    query = "MATCH (n:Chile)-->(p) WHERE n.screen_name={sn} RETURN collect(p.id) as n"
    param = {'sn': seed}
    results = gdb.query(query, params=param, data_contents=True)
    if len(results.rows) > 1:
        print "WARNING: ID CON MAS DE UN NODO ASIGNADO. Id: " + str(id)
    return results.rows[0][0]


def create_user_node(gdb, user={}):
    try:
        u = user.copy()
        n = gdb.node()
        if u.get('followers_ids') is not None:
            del (u['followers_ids'])
        n.properties = u
        n.labels.add("User")
        if n.get('chile') is True:
            n.labels.add("Chile")
            if n.get('screen_name') == SEMILLA:
                n.labels.add("Semilla")
        else:
            n.labels.add("Extranjero")
    except exceptions.StatusException as e:
        n.delete()
        print "It get next error: " + e.result
        return None
    print "Node %d successfully created " % u['id']
    return n


def get_list_users(gdb):
    query = "MATCH (n:User) RETURN n LIMIT 25"
    results = gdb.query(query, data_contents=True)
    return results


def get_user_node_by_id(gdb, id):
    query = "MATCH (n:User)WHERE n.id={id} RETURN n LIMIT 25"
    param = {'id': id}
    results = gdb.query(query, params=param, data_contents=True)
    if results.rows is not None:
        u = results.rows[0][0]


def get_id_user_node(gdb, id):
    query = "MATCH (n:User) WHERE n.id={id} RETURN {id: ID(n)} as n"
    param = {'id': id}
    results = gdb.query(query, params=param, data_contents=True)
    if len(results.rows) > 1:
        print "WARNING: ID CON MAS DE UN NODO ASIGNADO. Id: " + str(id)
    return results.rows[0][0]['id']


def get_user(gdb, id_user):
    exist = False  # To prevent repeating nodes
    # USE SQL
    results = get_user_sql(gdb, id_user)
    if len(results) >= 1:
        u = results[0]
        u['chile'] = True if len(get_user_location_sql(gdb, id_user)) > 0 else False
        return u
    # USE JSON
    user_file_name = os.path.join(BDJSON, str(id_user) + '.json')

    if os.path.exists(user_file_name):
        user = json.loads(file(user_file_name).read())
        return user
    # USE API TWITTER
    u = get_user_twitter(id_user)

    if u is None:
        return None

    if u.protected is True:
        return None

    user = {'location': u.location, 'id': id_user}
    user = is_location(user)
    user['screen_name'] = unicode(u.screen_name).encode('utf-8')
    user['followers_count'] = int(u.followers_count)
    user['followers_ids'] = u.followers_ids()
    user['time_zone'] = unicode(u.time_zone).encode('utf-8')
    user['geo_enabled'] = u.geo_enabled
    user['description'] = unicode(u.description).encode('utf-8')
    user['friends_count'] = int(u.friends_count)
    user['url'] = str(u.url)
    user['name'] = unicode(u.name).encode('utf-8')
    if user['chile'] is True:
        create_user_json(user, user_file_name)
    return user


def get_relation_by_id(gdb, id):
    query = "MATCH ()-[role:Follower]->() where role.id={id} return role"
    param = {'id': id}
    results = gdb.query(query, params=param, data_contents=True)
    return results.rows


def create_relation(gdb, node1, node2):
    idd = str(node1.id) + "r" + str(node2.id)
    relation = get_relation_by_id(gdb, idd)
    if relation is None:
        relation = node1.relationships.create("Follower", node2, id=idd)
        print "Relation between " + idd + " create."
    return relation


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

        while True:
            try:

                user = get_user(gdb, centre)
                if user is None or user['chile'] is False:
                    return taboo_list
                print 'user id %s' % str(centre)
                break
            except tweepy.TweepError, error:
                print type(error)

                if str(error) == 'Not authorized.':
                    print 'No se puede acceder a los datos de usuario - no autorizado.'
                    return taboo_list

                if str(error) == 'User has been suspended.':
                    print 'Usuario suspendido.'
                    return taboo_list

                errorObj = error[0][0]

                print errorObj

                if errorObj['message'] == 'Rate limit exceeded':
                    print 'Rate limited. Dormir durante 15 minutos.'
                    time.sleep(15 * 60 + 15)
                    continue

                return taboo_list

        cd = current_depth

        ids_loser = get_id_lost_users_sql(gdb)

        set_id_loser = set(ids_loser)
        setSemilla = set(get_ids_by_seed(gdb, str(user['screen_name'])))
        setFollowerId = set(user['followers_ids'])

        followerids = list(setFollowerId - setSemilla - set_id_loser)
        if cd + 1 < max_depth:
            idnodo = get_id_user_node(gdb, user['id'])
            nodo = gdb.node[idnodo]
            for fid in followerids[:int(FOLLOWERS_OF_FOLLOWERS_LIMIT)]:
                global FID
                FID = fid
                user2 = None
                while True:
                    try:
                        user2 = get_user(gdb, fid)
                        break
                    except tweepy.TweepError, e:
                        print "Primero: " + e.reason + " Termina."
                        if e.reason == 'Failed to send request: (\'Connection aborted.\', gaierror(-2, \'Name or service not known\'))':
                            print 'Internet. Dormir durante 1 minuto. ' + e.message
                            time.sleep(60)
                            continue
                        if e.reason == 'Failed to send request: HTTPSConnectionPool(host=\'api.twitter.com\', port=443): Read timed out. (read timeout=60)':
                            print 'Internet. Dormir durante 1 minuto. ' + e.message
                            time.sleep(60)
                            continue
                        if e.message[0]['code'] == 34:
                            print "Not found ApiTwitter id: " + str(centre) + " fid= " + str(fid)
                            cn = get_connection_sql()
                            insert_lost_user(cn, fid)
                            close_connection_sql(cn)
                            break
                        if e.message[0]['code'] == 63:
                            print 'Usuario suspendido:' + str(centre) + " fid= " + str(fid)
                            cn = get_connection_sql()
                            insert_lost_user(cn, fid)
                            close_connection_sql(cn)
                            break
                        else:
                            global ID_BAD
                            if ID_BAD == fid:
                                print "Id: %d durmio dos veces." % fid
                                break
                            ID_BAD = fid
                            # hit rate limit, sleep for 15 minutes
                            print 'Rate limited. Dormir durante 15 minutos. ' + e.reason
                            time.sleep(15 * 60 + 15)
                            continue
                    except StopIteration:
                        break

                if user2 is None:
                    continue

                idnodo2 = get_id_user_node(gdb, user2['id'])
                nodo2 = gdb.node[idnodo2]

                create_relation(gdb, nodo, nodo2)
                taboo_list = get_follower_ids(fid, max_depth=max_depth,
                                              current_depth=cd + 1, taboo_list=taboo_list)

        if cd + 1 < max_depth and len(followerids) > FOLLOWERS_OF_FOLLOWERS_LIMIT:
            print 'No todos los seguidores fueron recuperados para %d.' % centre

    except Exception, error:
        print 'Error al recuperar los seguidores de usuario id: ' + str(centre) + " fid = " + str(FID)
        print error
        return taboo_list
        sys.exit(1)

    return taboo_list


def main():
    screen_name = SEMILLA
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
