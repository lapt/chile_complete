# -*- coding: utf-8 -*-
import tweepy
from entities_db.Users import *
import time

__author__ = 'luisangel'

KEYS = [['rPTRg07wGJd1yARpwZpSyCfES', 'FFJBhKbvZvKWumQ2GfyNDS6BFba5O8xbReIieABm36M1nBbrXT',
         '126471512-6KjALSw2QNSoyQKPeTsmIomJpTJIR7b6cqjbPEY7', 'zog4rIcDoxezAelKK6cEoPeR4az77lvWUiscvoU2hP6iU'],
        ['sUTaliaIN6dBZqfsXWbVIUsh0', 'MQLE9w0g9VOE8LXsUZq4r2EFUTTgg5SjsG9mUMOaDcX0b1Cdxi',
         '126471512-hrDRXTqmyn2WMYxcPthu5OHLKMXxexbXHmWVMM22', 'k2ZSx0WeM5kR9FboUu3k9cCCNjrKSWoc8NbusOVin5Gub'],
        ['FbFWUyQieOv3al3Q6Ep9rO6jK', 'FUVqHHkTNc7yuyhwJUIxE1O7jYLjNWsKf3hZDaxvbu3RTCJcIm',
         '126471512-7IiwJ37n1GUUlXkIKESHIH96W4AV2XTRdgvg3yKj', 'mlDfER1EK5vnevRnUzCamez0fIni6GZKQQnLZ0M0Y7hen'],
        ['m4GuEho04oBvJ8XC0MvAJfNFr', 'ODaVqM3Gl9mYG7FIoIrJ74paGlQ0TCbA4n4L0TnuiJrZmVnIb3',
         '126471512-XBd0OOLCTgNXRdeVxaiZL3kG7mk93vX2yU71ADZl', 'XpsRytyHV7KvRws8uPnbFZqYbx3mNO4NfHcfxdRSViq89'],
        ['tAHAqgBoe3d7BKjwcUbD96Ayo', 'Apmf5Fl3QOOkXdGxMRprJiDjElfcLEXPsSR3TGGhXXBqUuGr7F',
         '126471512-t7oJ3DQMf8v7WuPNNsYqctErxHIzkgpDIb6MJlHS', 'LThvYHGQsXfZbf8sq4QyOOT6Oo7ajWQOai1J2pRGNr3Vp']
        ]
ID_KEY = 0
ID_BAD = 0
auth = tweepy.OAuthHandler(KEYS[ID_KEY][0], KEYS[ID_KEY][1])
auth.set_access_token(KEYS[ID_KEY][2], KEYS[ID_KEY][3])
api = tweepy.API(auth)


def get_new_api():
    global ID_KEY
    ID_KEY = 0 if ID_KEY >= 4 else ID_KEY + 1
    global auth
    auth = tweepy.OAuthHandler(KEYS[ID_KEY][0], KEYS[ID_KEY][1])
    auth.set_access_token(KEYS[ID_KEY][2], KEYS[ID_KEY][3])
    global api
    api = tweepy.API(auth)


def get_user_twitter(id_user):
    u = None
    while True:
        try:
            u = api.get_user(id_user)
            break
        except tweepy.TweepError, e:
            print "Primero: " + e.reason + " Termina."
            if e.reason == 'Failed to send request: (\'Connection aborted.\', ' \
                           'gaierror(-2, \'Name or service not known\'))':
                print 'Internet. Dormir durante 1 minuto. ' + e.message
                time.sleep(60)
                continue
            if e.reason == "Failed to send request: ('Connection aborted.', gaierror(-3, " \
                           "'Temporary failure in name resolution'))":
                print 'Internet. Dormir durante 1 minuto. ' + e.message
                time.sleep(60)
                continue
            if e.reason == 'Failed to send request: HTTPSConnectionPool(host=\'api.twitter.com\', port=443): ' \
                           'Read timed out. (read timeout=60)':
                print 'Internet. Dormir durante 1 minuto. ' + e.message
                time.sleep(60)
                continue
            if e.reason == "Failed to send request: ('Connection aborted.', BadStatusLine(\"''\",))":
                print 'Internet. Dormir durante 1 minuto. ' + e.message
                time.sleep(60)
                continue
            if e.message[0]['code'] == 34:
                print "Not found ApiTwitter id: " + str(id_user)
                cn = get_connection_sql()
                insert_lost_user(cn, id_user)
                cn.close()
                break
            if e.message[0]['code'] == 63:
                print 'Usuario suspendido:' + str(id_user)
                cn = get_connection_sql()
                insert_lost_user(cn, id_user)
                cn.close()
                break
            if e.message[0]['code'] == 50:
                print 'User not found:' + str(id_user)
                cn = get_connection_sql()
                insert_lost_user(cn, id_user)
                cn.close()
                break
            else:
                global ID_BAD
                if ID_BAD == id_user:
                    print "Id: %d durmio dos veces." % id_user
                    break
                ID_BAD = id_user
                # hit rate limit, sleep for 15 minutes
                print 'Rate limited. Dormir durante 15 minutos. code: ' + ' id: ' + str(id_user)
                get_new_api()
                continue
        except StopIteration:
            break

    return u