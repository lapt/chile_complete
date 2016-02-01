# -*- coding: utf-8 -*-
import tweepy

__author__ = 'luisangel'

KEYS = [['2c29GszJSIOm3eC2DTwnLstit', 'PjEYEULB6J43DAJQeoSm7xBpAWG31iEU0r5KkOjrgEYJZzTKyd',
          '126471512-xy5VaQkjrot03QCLIcl2FuehFnNBo3FrXAjJNOxp', 'yN5y1r22z3hv5wDRRlzzsxPWCUITxe3Z5b7KO7wognSbz'],
         ['HFvyfF6HwRmiTmPUzyDfEEQjN', 'm2NBerSxyry71jSciVxxFBT0gD7qyVo8xHK4HIhWHQYZGWz4ey',
          '126471512-rUxowItDqWG4JJ4QykaIIU5nZxNhlev7X1J9AfOd', 'MCrfnd7O4Hebrl1eFbNKg8u7Wsu3AHdutoUnEI0pXh84D'],
         ['1JGzkqZfnvwoNm1qJrrR84y8Z', 'kCtINE8ODZNsRh3XZRVWPkoyXGwpLQeAs81B1mOy84Vd5qlvlE',
          '126471512-rxzPdA2cDHe3XIv2qypZocaCBJTWBEfPaRqulPq7', 'uAR4wnRga76FUOKI9qaNOHjgiNhhwHMyHLDXrnZOG2Cz3'],
         ['hxWTVmGUUqQHSwyCNqGf8qJHq', 'SwRTpWc9aMrUHJfaZ7YItFaEuhk37GAedXDidhNvMN5KkqoJa8',
          '126471512-2liUkz8sixVZYnPRfDHWettlyqsgZUEosBWbWzPC', '7FXKu4dXir9GM1j9PvwwLSnRwoLPC3yeW00vxRLWwg6GJ'],
         ['EZVUeCrKoezDMi34UPZBMXQYf', 'Lm8CKkPFgn1uTVcsPAwZHQoBmXEQMbsKjnHbUqteAWfyyBS8wd',
          '126471512-m3YNr4C6w3ZqmRIntIA5k2K5fKS3ZYqWMDCiFV5g', '8UX7j6HHWwUplXUPgjhmtn3K9T5eIl4jY4URUMJkYqToN']
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