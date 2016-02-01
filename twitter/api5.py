# -*- coding: utf-8 -*-
import tweepy

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

auth = tweepy.OAuthHandler(KEYS[ID_KEY][0], KEYS[ID_KEY][1])
auth.set_access_token(KEYS[ID_KEY][2], KEYS[ID_KEY][3])
api = tweepy.API(auth)