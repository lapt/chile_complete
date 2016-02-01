# -*- coding: utf-8 -*-
import tweepy

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

auth = tweepy.OAuthHandler(KEYS[ID_KEY][0], KEYS[ID_KEY][1])
auth.set_access_token(KEYS[ID_KEY][2], KEYS[ID_KEY][3])
api = tweepy.API(auth)