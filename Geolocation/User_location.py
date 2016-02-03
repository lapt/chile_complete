#!/usr/bin/python
# -*- coding: utf-8 -*-
import unicodedata

from location_cleaner import *
from Geolocation.geo_db_connector import *
from geodict.geodict_lib import get_city_by_name


__author__ = 'luisangel'

GEO_NOM = ['scl', 'chile', 'cl', 'chl', 'stgo', 'santiasco']


def delete_tildes(s=''):
    return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))


def clean_string(text=''):
    text = text.lower()
    text = delete_tildes(text.decode('utf-8'))
    return text


def is_location(gdb, data={}, cities={}):
    if data['location'] is None or len(data['location'].strip()) == 0:
        data['chile'] = False
        return data

    place = data['location']
    place = u''.join(place).encode('utf-8').strip()

    place = clean_string(place)

    if len(place.strip()) == 0:
        data['chile'] = False
        return data

    # =============coordinate====

    if hasCoordinates(place) is True:
        geo = cleanLocationField(place)
        location = getClosestCityAdmins(gdb, geo.getLatitude(), geo.getLongitude(), 100)
        data['country_code'] = location[0]
        data['region_code'] = location[1]
        data['longitude'] = geo.getLongitude()
        data['latitude'] = geo.getLatitude()
        data['chile'] = True
        return data

    # ============Mysql=================

    for city in cities:
        city_name = unicode(city['city_name']).encode('utf-8')
        if place.find(city_name) >= 0:
            data['country_code'] = unicode(city['country_code']).encode('utf-8')
            data['region_code'] = unicode(city['region_code']).encode('utf-8')
            data['longitude'] = city['longitude']
            data['latitude'] = city['latitude']
            data['chile'] = True
            return data

    # =========== Others ======

    for linea in GEO_NOM:
        if place.find(linea) >= 0:
            chile = get_city_by_name(gdb, 'santiago')
            data['country_code'] = unicode(chile[0]['country_code']).encode('utf-8')
            data['region_code'] = unicode(chile[0]['region_code']).encode('utf-8')
            data['longitude'] = chile[0]['longitude']
            data['latitude'] = chile[0]['latitude']
            data['chile'] = True
            return data

    data['chile'] = False
    return data
