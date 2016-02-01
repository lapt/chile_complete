# -*- coding: utf-8 -*-
import tweepy


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