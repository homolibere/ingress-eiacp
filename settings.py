__author__ = 'homolibere'

import os.path

import ConfigParser

login_url = 'https://accounts.google.com/ServiceLogin?service=ah&passive=false&continue=https://appengine.google.com/_ah/conflogin%3Fcontinue%3Dhttps://www.ingress.com/intel&ltmpl=gm'
chat_url = 'http://www.ingress.com/rpc/dashboard.getPaginatedPlextsV2'
score_url = 'http://www.ingress.com/rpc/dashboard.getGameScore'
post_data = None
request_headers = {'User-agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
result = {}

def load_config():
    if os.path.exists('config.cfg'):
        config = ConfigParser.RawConfigParser()
        config.read('config.cfg')
        # db section
        result['db_host'] = config.get('DB', 'db_host')
        result['db_port'] = config.get('DB', 'db_port')
        result['db_user'] = config.get('DB', 'db_user')
        result['db_passwd'] = config.get('DB', 'db_passwd')
        result['db_name'] = config.get('DB', 'db_name')
        #general section
        result['cookie_file_path'] = config.get('general', 'cookie_file_path')
        result['ingress_login'] = config.get('general', 'ingress_login')
        result['ingress_pass'] = config.get('general', 'ingress_pass')
        result['smtp_server'] = config.get('general', 'smtp_server')
        result['smtp_port'] = config.get('general', 'smtp_port')
        result['timeout'] = config.getint('general', 'timeout')
        result['use_gtalk'] = config.getint('general', 'use_gtalk')
    else:
        raise Exception("No configuration file found")
    return result
