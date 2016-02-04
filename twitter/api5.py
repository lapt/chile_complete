# -*- coding: utf-8 -*-
import tweepy
from entities_db.Users import *
import time

__author__ = 'luisangel'

KEYS = [['1aUE01m6RTZZntyfSAJSI8NwG', 'jwggsJbyz7bJpkFAvVRNFq1eMWTEdUYBXLXP8tmCf0sH2zZIdc',
         '126471512-12bRUjQjr5bDyIoL3gA6Wq1J0byRhh1MuQzDeaC3', 'wojWtKHGHkvqVc3KSvLliWP2U4qQlweQrMcjWbQVGmhMM'],
        ['Ko7HB8uECkVvd3hsiVRukb0lg', 'tVRyWEa4J0Yw9KBLzZMp2QOCoiaahClxAPNASN4Lwl2SfhIh8w',
         '126471512-OEmy4bcwiTfrPR1LljUUNtaDs33VUnhw3NB7oxXv', 'ZMqVs24giY7T2dMB2yA4Sdn0iz1yurIND2Eh44KPyl8fx'],
        ['Mk8X14g5E7XAqw3tWcNZiMLn3', 'r0NsM8CrwlHhZqI7niNh96M5OlfGFzxwHBBoksqYKgaDlOl7HS',
         '126471512-nDp9VF09ouMcYp4HC13shKhCDxKlFP1SeWyoJGBi', 'mCW9FvQAQCdHT2imaoSl5hSZtcGQfUnQ5w5EtqUxFWSrZ'],
        ['yDyQ2r8ygIYWG0nHqccMdYdZ1', '1AmCaMtC3XprLEwE7vhmSX6J0iCIe02kODXznfsbcp62mTvFo6',
         '126471512-eNGOjOEbV1B3nzbz3oWX2S1OEvwioguEOmjiQW6I', '1aniqa6EgGLjGyvnDoyUksnHoecBgirzzxoHWnswjKhBg'],
        ['EC007SKfmmVgn1BrKNr1Yziyh', 'Te07yqZJdhnr203Pk9jQB1M8eteH1F3gy8BjOKebsZhYxpvU7L',
         '126471512-76uE3zktCRzekZXWttc8GsezUn2BKYMmYjhhVVlf', 'g6miC1CBYuILAw8Ri8jFbx1YYtTaYKKrHgIbncVd5wEgS']
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