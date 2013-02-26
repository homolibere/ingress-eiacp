__author__ = 'homolibere'

import threading
import re
import pymysql

import settings
import notification

portals_ins_sql = "INSERT IGNORE INTO statistic (player_guid) VALUES (%s);"

portal_owner_upd_sql = "UPDATE ingress_portals SET owner = %s WHERE guid = %s;"
player_level_upd_sql = "UPDATE ingress_players SET player_level = %s WHERE guid = %s and IFNULL(player_level, 0) < %s"

inc_res_dep_upd_sql = "UPDATE statistic SET resonators_dep = resonators_dep + 1 WHERE player_guid = %s"
inc_res_des_upd_sql = "UPDATE statistic SET resonators_des = resonators_des + 1 WHERE player_guid = %s"
inc_lnk_dep_upd_sql = "UPDATE statistic SET links_dep = links_dep + 1 WHERE player_guid = %s"
inc_lnk_des_upd_sql = "UPDATE statistic SET links_des = links_des + 1 WHERE player_guid = %s"
inc_cfld_dep_upd_sql = "UPDATE statistic SET control_fld_dep = control_fld_dep + 1 WHERE player_guid = %s"
inc_cfld_des_upd_sql = "UPDATE statistic SET control_fld_des = control_fld_des + 1 WHERE player_guid = %s"
inc_pcap_upd_sql = "UPDATE statistic SET portal_cap = portal_cap + 1 WHERE player_guid = %s"

notif_sel_sql = "SELECT n.to_mail, n.to_jabber, u.user_email, u.user_jabber FROM notification AS n JOIN users AS u ON n.to_user_id = u.user_id WHERE n.guid = %s"

class process_data_thread(threading.Thread):

    def __init__(self, params):
        threading.Thread.__init__(self)
        self.event_guid = params[0]
        self.time_stamp = params[1]
        self.user_guid = params[2]
        self.portal_from_guid = params[3]
        self.portal_to_guid = params[4]
        self.plext_text = params[5]
        self.action_type = params[6]
        self.plext_type = params[7]
        self.plext_team = params[8]
        self.is_secured = params[9]
        self.conn = None
        cfg = settings.load_config()
        self.conn = pymysql.connect(host = cfg['db_host'], port = int(cfg['db_port']), user = cfg['db_user'],\
            passwd = cfg['db_passwd'], db = cfg['db_name'])

    def update_portal_owner(self, params):
        cur = self.conn.cursor()
        cur.execute(portal_owner_upd_sql, params)
        cur.connection.commit()
        cur.close()

    def update_player_level(self, params):
        cur = self.conn.cursor()
        cur.execute(player_level_upd_sql, params)
        cur.connection.commit()
        cur.close()

    def insert_player_stat(self, params):
        cur = self.conn.cursor()
        cur.execute(portals_ins_sql, params)
        cur.connection.commit()
        cur.close()

    def update_player_stat_rdep(self, params):
        cur = self.conn.cursor()
        cur.execute(inc_res_dep_upd_sql, params)
        cur.connection.commit()
        cur.close()

    def update_player_stat_rdes(self, params):
        cur = self.conn.cursor()
        cur.execute(inc_res_des_upd_sql, params)
        cur.connection.commit()
        cur.close()

    def update_player_stat_ldep(self, params):
        cur = self.conn.cursor()
        cur.execute(inc_lnk_dep_upd_sql, params)
        cur.connection.commit()
        cur.close()

    def update_player_stat_ldes(self, params):
        cur = self.conn.cursor()
        cur.execute(inc_lnk_des_upd_sql, params)
        cur.connection.commit()
        cur.close()

    def update_player_stat_cfdep(self, params):
        cur = self.conn.cursor()
        cur.execute(inc_cfld_dep_upd_sql, params)
        cur.connection.commit()
        cur.close()

    def update_player_stat_cfdes(self, params):
        cur = self.conn.cursor()
        cur.execute(inc_cfld_des_upd_sql, params)
        cur.connection.commit()
        cur.close()

    def update_player_stat_pcap(self, params):
        cur = self.conn.cursor()
        cur.execute(inc_pcap_upd_sql, params)
        cur.connection.commit()
        cur.close()

    def check_guid_notification(self, guid):
        cur = self.conn.cursor()
        cur.execute(notif_sel_sql, guid)
        for subscriber_data in cur.fetchall():
            if subscriber_data[0] == 1:
                notification.send_mail_message(subscriber_data[2], self.plext_text)
            if subscriber_data[1] == 1:
                notification.send_jabber_invitation(subscriber_data[3])
                notification.send_jabber_message(subscriber_data[3], self.plext_text)
        cur.connection.commit()
        cur.close()

    def run(self):
        if self.action_type in [1, 2, 4, 5, 6, 7, 8]:
            if self.portal_to_guid <> None:
                self.check_guid_notification(self.portal_to_guid)
            if self.portal_from_guid <> None:
                self.check_guid_notification(self.portal_from_guid)
            if self.user_guid <> None:
                self.check_guid_notification(self.user_guid)
            self.insert_player_stat((self.user_guid))
            if self.action_type == 1:
                self.update_player_stat_cfdep((self.user_guid))
            if self.action_type == 2:
                self.update_player_stat_cfdes((self.user_guid))
            if self.action_type == 4:
                match = re.search('L([0-9]{1})', self.plext_text)
                if match:
                    resonator_level = match.group()[1:]
                    self.update_player_level((int(resonator_level), self.user_guid, int(resonator_level)))
                self.update_player_stat_rdep((self.user_guid))
            if self.action_type == 5:
                self.update_player_stat_rdes((self.user_guid))
            if self.action_type == 6:
                self.update_portal_owner((self.user_guid, self.portal_from_guid))
                self.update_player_stat_pcap((self.user_guid))
            if self.action_type == 7:
                self.update_player_stat_ldep((self.user_guid))
            if self.action_type == 8:
                self.update_player_stat_ldes((self.user_guid))
