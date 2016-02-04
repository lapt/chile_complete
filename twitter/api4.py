# -*- coding: utf-8 -*-
import tweepy
from entities_db.Users import *
import time
__author__ = 'luisangel'

KEYS = [['pmsHi3fTyJrqQ6Ov0ANudX2jd', 'r1sIVRwLumaCJZenTrrQK4HdHaLn749dBeBfl4zx61DsvE3ySH',
         '126471512-ld4Cn3Btt4Jbt3hJjXpJep7u9rDFzt8nX6MtxcMa', 'jVDKc4ZBpCfvkGSt7CO44s1mKzfUu4c96E8QNRm0Br80w'],
        ['jDg9LNtVVgqBQnZ3TnyadcpvV', 'gKirPUeRfJvF9b8atUOYbVZt5N5XR4Mn0BALj3VAjkJMtZQbSf',
         '126471512-XjsMgivyCmVgMq2QB6iQhKYnNPWT1dUklpsALZ6n', 'CdbLC9vh2d6xNjy6U5KV80DVoBHvlU2YzahuYg1QoXHWt'],
        ['rN4pHBr2owpAxvtnNGuk89PkD', 'Ham1VLOqJo215Rr9Iczv0rJhFxZRXsOTjACStUtYFgsKntMghl',
         '126471512-kIScTpVMqT5GDLKO089JVsEcwSniSEANCgahMBfw', 'YhixBt4m7d5kdp60HtaOTWeI6qjxjxo0qezL887pImz2h'],
        ['QjBYJl9mapJBHrf3HJTYemHIi', 'UUaOitJpHZWAS026fbqzjAUWPsY8FJf5VvycCwDjXSqAIpheZY',
         '126471512-4aJQ4pBXoE7ADoWqQ3Sms3SvaDCYhQlJEnjqQ2U5', 'ZBvbDXB1BAjh3zWnLZG7AW1QyHvaQAHHTF3iUoMRLdtFX'],
        ['N0FOjQ0nM1aZE5J2x281ceCXC', '39T7HICkYlumTUIziQhP9gQaHATwUmmACeioe3xFN1DmqllFJP',
         '126471512-sFqNbzR2CkAc1cbO7yb6z6SnnjEPNaP9xRLbATHx', 'FjbQ03CFFLlVQOhyzbn8Lx5Bxw4gCL9EyOghgS5t1zJnE']
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