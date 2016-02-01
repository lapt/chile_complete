# -*- coding: utf-8 -*-

from Geolocation.geo_db_connector import *
from Geolocation.location_cleaner import *
import re

__author__ = 'luisangel'


def main():

    gdb = getConnection()
    result = getClosestCityAdmins(gdb, -24.809020, -70.229539, 100)
    print result

if __name__ == '__main__':
    main()
