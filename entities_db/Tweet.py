import MySQLdb

__author__ = 'luisangel'


def get_id_tweet_by_id_user(connection, id_user):
    query = "SELECT idTweet FROM Tweet where idUser=%s order by idTweet desc limit 1;"
    try:
        cursor = connection.cursor()
        cursor.execute(query, (id_user,))
        data = cursor.fetchone()
        if data is None:
            return None
        else:
            return data[0]
    except MySQLdb.Error:
        print "Error: unable to fetch data"
        return -1


def count_tweets(connection, id_user):
    query = "select count(*) from Tweet where idUser=%s;"
    try:
        cursor = connection.cursor()
        cursor.execute(query, (id_user,))
        data = cursor.fetchone()
        if data is None:
            return None
        else:
            return data[0]
    except MySQLdb.Error:
        print "Error: unable to fetch data"
        return -1


def get_tweets(connection):
    query = "SELECT Tweet.text FROM Tweet;"
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        if data is None:
            return None
        else:
            for t in data:
                print t[0]
    except MySQLdb.Error:
        print "Error: unable to fetch data"
        return -1


def insert_tweets(connection, tweet, id_user, id_region):
    try:
        data = count_word_tweet(tweet)
        x = connection.cursor()
        x.execute('INSERT INTO Tweet VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ', (
            tweet.id_str, tweet.created_at, tweet.text.encode("utf-8"),
            1 if tweet.favorited is True else 0,
            tweet.favorite_count, 1 if tweet.truncated is True else 0, id_user, tweet.retweet_count,
            1 if tweet.retweeted is True else 0, id_region,
            data['gato'], data['aroa'], data['RT'], data['URL']))
        connection.commit()
    except MySQLdb.DatabaseError, e:
        print 'Error %s' % e
        connection.rollback()


def count_word_tweet(tw):
    w = tw.entities
    count = {'aroa': len(w['user_mentions']), 'gato': len(w['hashtags']), 'URL': len(w['urls']),
             'RT': int(hasattr(tw, 'retweeted_status'))}
    return count