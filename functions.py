#-*- coding: utf-8 -*-
from datetime import date, timedelta

def getYesterday():
    yesterday = date.today() - timedelta(1)
    date_String = yesterday.strftime('%Y%m%d')
    return date_String

def sortAdwClicksSessions(json_Data):
    yesterday = getYesterday()
    data_Dict = [x for x in json_Data if x['dimension'][1] == yesterday]
    source_Dict = [x for x in data_Dict if x['dimension'][0] == 'google / cpc']
    network_Dict = [x for x in source_Dict if x['dimension'][2] != 'Content']
    adw_Clicks_Arr = [x['value'] for x in network_Dict if x['name'] == 'ga:adClicks']
    adw_Sessions_Arr = [x['value'] for x in network_Dict if x['name'] == 'ga:sessions']
    adw_Clicks = 0
    adw_Sessions = 0
    for values in adw_Clicks_Arr:
        adw_Clicks = adw_Clicks+float(values)
    for values in adw_Sessions_Arr:
        adw_Sessions = adw_Sessions+float(values)
    try:
        adw_Clicks = float(adw_Clicks)
    except IndexError:
        adw_Clicks = 0
    try:
        adw_Sessions = float(adw_Sessions)
    except IndexError:
        adw_Sessions = 0
    return {"adw_Clicks":adw_Clicks, "adw_Sessions":adw_Sessions}

def sortSessions30Total(json_Data):
    source_Dict = [x for x in json_Data if x['dimension'][0] == 'google / organic']
    sessions_Dict = [x for x in source_Dict if x['name'] == 'ga:sessions']
    total_Sessions = 0
    for values in sessions_Dict:
        total_Sessions = total_Sessions+int(values['value'])
    try:
        return float(total_Sessions)
    except IndexError:
        return 0

def sortSessionsYesterday(json_Data):
    yesterday = getYesterday()
    source_Dict = [x for x in json_Data if x['dimension'][0] == 'google / organic']
    data_Dict = [x for x in source_Dict if x['dimension'][1] == yesterday]
    sessions_Dict = [x for x in data_Dict if x['name'] == 'ga:sessions']
    try:
        return float(sessions_Dict[0]['value'])
    except IndexError:
        return 0