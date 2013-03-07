__author__ = 'homolibere'

import json
import database
import logging

log = logging.getLogger(__name__)

def parse_score_to_db(input_data):
    json_data = json.loads(input_data)
    database.init_connection()
    aliens_score = json_data['result']["alienScore"]
    resistance_score = json_data['result']["resistanceScore"]
    database.insert_score((int(aliens_score), int(resistance_score)))

def parse_chat_to_db(input_data):
    json_data = json.loads(input_data)
    if json_data.get('error'):
        log.error(json_data['error'])
    else:
        database.init_connection()
        #-1 - unknown action
        #0 - user message
        #1 - control field created
        #2 - control field destroyed
        #3 - control field decayed
        #4 - resonator deployed
        #5 - resonator destroyed
        #6 - portal captured
        #7 - link created
        #8 - link destroyed
        #9 - destroyed portal mod
        for result_node in json_data['result']:
            action_type = -1
            message_guid = result_node[0]
            time_stamp = result_node[1]
            plext = result_node[2]["plext"]
            plext_type = plext["plextType"]
            plext_team = plext["team"]
            plext_text = plext["text"]
            markup = plext["markup"]
            user_guid = None
            user_plain = None
            user_team = None
            portal_to = None
            portal_to_adress = None
            portal_to_guid = None
            portal_to_lat = None
            portal_to_lng = None
            portal_to_name = None
            #unused so far
            portal_to_team = None
            portal_from = None
            portal_from_adress = None
            portal_from_guid = None
            portal_from_lat = None
            portal_from_lng = None
            portal_from_name = None
            #unused so far
            portal_from_team = None
            is_secured = 0
            if plext_type == 'PLAYER_GENERATED':
                action_type = 0
                for markup_node in markup:
                    if markup_node[0] == "SECURE":
                        is_secured = 1
                    if markup_node[0] == "SENDER":
                        user_guid = markup_node[1]["guid"]
                        if markup_node[1]["plain"].find(':') > -1:
                            user_plain = markup_node[1]["plain"][:-2]
                        else:
                            user_plain = markup_node[1]["plain"]
                        user_team = markup_node[1]["team"]
                    if markup_node[0] == "TEXT":
                        user_text = markup_node[1]["plain"]
            if plext_type == 'SYSTEM_BROADCAST':
                for markup_node in markup:
                    if markup_node[0] == "PLAYER":
                        user_guid = markup_node[1]["guid"]
                        if markup_node[1]["plain"].find(':') > -1:
                            user_plain = markup_node[1]["plain"][:-2]
                        else:
                            user_plain = markup_node[1]["plain"]
                        user_team = markup_node[1]["team"]
                    if (markup_node[0] == "PORTAL" and portal_from != None):
                        portal_to = markup_node[1]
                        portal_to_adress = markup_node[1]["address"]
                        portal_to_guid = markup_node[1]["guid"]
                        portal_to_lat = markup_node[1]["latE6"]
                        portal_to_lng = markup_node[1]["lngE6"]
                        portal_to_name = markup_node[1]["name"]
                        portal_to_team = markup_node[1]["team"]
                    if (markup_node[0] == "PORTAL" and portal_from == None):
                        portal_from = markup_node[1]
                        portal_from_adress = markup_node[1]["address"]
                        portal_from_guid = markup_node[1]["guid"]
                        portal_from_lat = markup_node[1]["latE6"]
                        portal_from_lng = markup_node[1]["lngE6"]
                        portal_from_name = markup_node[1]["name"]
                        portal_from_team = markup_node[1]["team"]
                if plext_text.find('created a Control Field') > -1:
                    action_type = 1
                if plext_text.find('destroyed a Control Field') > -1:
                    action_type = 2
                if (plext_text.find('Control Field') > -1 and plext_text.find('has decayed') > -1):
                    action_type = 3
                if plext_text.find('deployed an') > -1:
                    action_type = 4
                if plext_text.find('destroyed an') > -1:
                    action_type = 5
                if plext_text.find(' captured ') > -1:
                    action_type = 6
                if plext_text.find(' linked ') > -1:
                    action_type = 7
                if plext_text.find('destroyed the Link ') > -1:
                    action_type = 8
                if (plext_text.find('destroyed') > -1 and plext_text.find('Portal Mod') > -1):
                    action_type = 9
            from datetime import datetime
            full_params = (message_guid, datetime.fromtimestamp(int(time_stamp / 1000)), user_guid, portal_from_guid, portal_to_guid, \
                plext_text.encode('utf8'), int(action_type), plext_type, plext_team, is_secured)
            log.debug(full_params)
            if (user_guid <> None and user_plain <> None and user_team <> None):
                database.insert_player((user_guid, user_plain, user_team))
            if (portal_to <> None):
                database.insert_portal((portal_to_guid, portal_to_adress.encode('utf8'), int(portal_to_lat), int(portal_to_lng), portal_to_name.encode('utf8')))
            if (portal_from <> None):
                database.insert_portal((portal_from_guid, portal_from_adress.encode('utf8'), portal_from_lat, portal_from_lng, portal_from_name.encode('utf8')))
            database.insert_event(full_params)
        database.close_connection()
