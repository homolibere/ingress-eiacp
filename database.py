__author__ = 'homolibere'

import pymysql
import re
import string
import random
import data_processing
import datetime

import settings
import notification

portals_ins_sql = "INSERT IGNORE INTO ingress_portals (guid, address, latE6, lngE6, name) VALUES (%s,%s,%s,%s,%s);"
users_ins_sql = "INSERT IGNORE INTO ingress_players (guid, plain, team) VALUES (%s,%s,%s);"
event_ins_sql = "INSERT IGNORE INTO ingress_events (guid,timestamp,player_guid,portal_from_guid,portal_to_guid,event_plain_text, \
    event_action,event_type,event_team,event_is_secured) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
score_ins_sql = "INSERT IGNORE INTO ingress_score (score_date, score_resistance, score_aliens) VALUES (%s,%s,%s)"

select_reg_sql = "SELECT user_id, user_email FROM users WHERE upper(registration_code) = upper(%s) AND ingress_user_guid IS Null;"
upd_reg_sql = "UPDATE users SET ingress_user_guid = %s, user_passwd = md5(%s),registration_code = Null WHERE user_id = %s;"
select_reg_nickname_sql = "SELECT plain FROM ingress_players WHERE guid = %s"

conn = None

def check_user_registration(player_guid, plaxt_text):
    match = re.search('reg\:([A-Za-z0-9]{8})', plaxt_text)
    if match:
        global conn
        cur = conn.cursor()
        cur.execute(select_reg_sql, match.group()[4:])
        cur.connection.commit()
        user_credentials = cur.fetchone()
        if user_credentials <> None:
            passwd = temp_pass_generate()
            cur.execute(upd_reg_sql,(player_guid, passwd, user_credentials[0]))
            cur.connection.commit()
            cur.execute(select_reg_nickname_sql, player_guid)
            cur.connection.commit()
            user_nick = cur.fetchone()
            if user_nick <> None:
                notification.send_reg_mail(user_credentials[1], user_nick[0], passwd)
        cur.close()

def close_connection():
    global conn
    conn.close()
    conn = None

def init_connection():
    global conn
    if conn == None:
        cfg = settings.load_config()
        conn = pymysql.connect(host = cfg['db_host'], port = int(cfg['db_port']), user = cfg['db_user'],\
            passwd = cfg['db_passwd'], db = cfg['db_name'])

def insert_event(params):
    global conn
    if conn == None:
        init_connection()
    cur = conn.cursor()

#    0 - message_guid
#    1 - time_stamp
#    2 - user_guid
#    3 - portal_from_guid
#    4 - portal_to_guid
#    5 - plext_text
#    6 - action_type
#    7 - plext_type
#    8 - plext_team
#    9 - is_secured

    if cur.execute(event_ins_sql, params) > 0:
        if (params[6] == 0 and params[8] == 'ALIENS'):
            check_user_registration(params[2], params[5])
        process_th = data_processing.process_data_thread(params)
        process_th.start()
    cur.connection.commit()
    cur.close()

def insert_player(params):
    global conn
    if conn == None:
        init_connection()
    cur = conn.cursor()
    cur.execute(users_ins_sql, params)
    cur.connection.commit()
    cur.close()

def insert_portal(params):
    global conn
    if conn == None:
        init_connection()
    cur = conn.cursor()
    cur.execute(portals_ins_sql, params)
    cur.connection.commit()
    cur.close()

def insert_score(params):
    global conn
    if conn == None:
        init_connection()
    cur = conn.cursor()
    cur.execute(score_ins_sql, (datetime.datetime.now(), params[0], params[1]))
    cur.connection.commit()
    cur.close()

def temp_pass_generate(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))