# -*- coding: utf-8 -*-
import tweepy
from entities_db.Users import *
import time

__author__ = 'luisangel'

KEYS = [['NKNCueURlcpitCRUwK0TngfLq', 'HB7aKDAHwBSinXnfU7hKvFUKTpESfMPFm3YKtOyViTw8md4rhl',
         '126471512-It4hiXQFV5ar8wYIj5GTObuwwfbrjblxOzUS98Ah', '4g7tCdzP6ZvFm5hEPCi1oIvi45hepUAPWcqQX590a8BKG'],
        ['IX6Q6oe0RCXZ6QVmalDbDP7Oj', '4zfTRD9epY2CtWFNMP29FAjwDlpnp7dmg8sAsaadTh3Ow4Iw9z',
         '126471512-mJVuNoxQCj0JTLEgPaGP8Jf5TFet6MI0vR9TEeNN', 'VyhwIodgNGsHxsFaYEVuLDd85ZWZLfHXkOPtZFw0v3jNM'],
        ['7wlc3nNp5Hnmi3adSQYI39fot', 'q2Ia3unh8MNaAMPTcMPWYSHCLsqfWHd4mOgBP9BvuEhFt8860p',
         '126471512-01YsPw2OXopcYw1H8clZUwzGWzrrE4l3gIt4QqWj', 'MzNd5TZxzxKPwpUlZ1ldbPfr8su75hCxt359sCMVzK0SO'],
        ['CdLbvHLjTAeaHnKoWhTqtV6US', 'fpPcGAma22pnXMGRsNLSoKCF8oKPl7R5SlncbTQqVuuNVQtJNb',
         '126471512-ZHy14Tz4xWhFaNXoTOZDUBQ5D6NzyFc52ip9V0cB', 'Zfis0GQbcitJI27MFrCe8Uqascqt2tD3AJC0wKIUSUgzv'],
        ['gCrcxyVA0AQUkzlF32J4OoKy9', 'TLl3fJyWL1ULSGPFYfhh9x8qIunKDbfLB1mqoacQJ6A8g6cFSS',
         '126471512-yrwSJN9QVPGafAI4s7Adfu5cKpA5AAnLz4zIWUAx', 'foa09dwa6AXTC0IIzgOslL2UYfEVPd6Px0iDUfr9HkJTn']]
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
            if e.reason == "Twitter error response: status code = 503":
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
