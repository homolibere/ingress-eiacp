__author__ = 'homolibere'

import os.path
import sys
import settings
import urllib
import cookielib
import urllib2
import time
import traceback
import threading
import logging

import chat_parser
import notification

http_opener = urllib2.urlopen
cookie_stor = cookielib.LWPCookieJar()
http_request = urllib2.Request

cfg = settings.load_config()
log = logging.getLogger(__name__)

if os.path.isfile(cfg['cookie_file_path']):
    cookie_stor.load(cfg['cookie_file_path'])
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_stor))
urllib2.install_opener(opener)

class score_thread(threading.Thread):

    def get_score(self):
        csrftoken = None
        for index, cookie in enumerate(cookie_stor):
            if cookie.name == 'csrftoken':
                csrftoken = cookie.value
        try:
            if csrftoken == None:
                raise Exception("csrftoken not assigned")
            log.debug("execute: get_score")
            settings.post_data = '{"method":"dashboard.getGameScore"}'
            request_head = settings.request_headers
            request_head['Accept'] = 'application/json, text/javascript, */*; q=0.01'
            request_head['DNT'] = '1'
            request_head['Content-Type'] = 'application/json; charset=utf-8'
            request_head['X-Requested-With'] = 'XMLHttpRequest'
            request_head['Referer'] = 'http://www.ingress.com/intel'
            request_head['X-CSRFToken'] = csrftoken
            req = http_request(settings.score_url, settings.post_data, request_head)
            handle = http_opener(req)
        except IOError, e:
            log.error('We failed to open "%s".' % settings.score_url)
            if hasattr(e, 'code'):
                log.error('We failed with error code - %s. ' % e.code, settings.score_url)
                raise
            elif hasattr(e, 'reason'):
                log.error('The error object has the following "reason" attribute :' + e.reason)
                log.error("This usually means the server doesn't exist, is down, or we don't have an internet connection.")
                sys.exit()
        else:
            return handle.read()

    def run(self):
        time.sleep(20)
        while True:
            score_json = self.get_score()
            try:
                chat_parser.parse_score_to_db(score_json)
            except:
                log.error('json:' + score_json)
                log.error('Unexpected error:' + traceback.format_exc())
            time.sleep(3600)

class chat_thread(threading.Thread):

    def login_and_get_cookies(self):
        log.debug("execute: login_and_get_cookies")
        print time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()), " : ", "login in ingress", settings.login_url
        if os.path.isfile(cfg['cookie_file_path']):
            os.remove(cfg['cookie_file_path'])
        settings.post_data = None
        try:
            req = http_request(settings.login_url, settings.post_data, settings.request_headers)
            handle = http_opener(req)
        except IOError, e:
            print 'We failed to open "%s".' % settings.login_url
            if hasattr(e, 'code'):
                log.error('We failed to open "%s".' % settings.login_url)
            elif hasattr(e, 'reason'):
                log.error('The error object has the following "reason" attribute :' + e.reason)
                log.error("This usually means the server doesn't exist, is down, or we don't have an internet connection.")
                sys.exit()
        cookie_stor.save(cfg['cookie_file_path'])
        from HTMLParser import HTMLParser
        # create a subclass and override the handler methods
        class MyHTMLParser(HTMLParser):
            input_dsh = None
            input_galx = None
            def handle_starttag(self, tag, attrs):
                if (tag == 'input' and attrs[1][0] == 'name' and attrs[1][1] == 'dsh'):
                    self.input_dsh = attrs[3][1]
                if (tag == 'input' and attrs[1][0] == 'name' and attrs[1][1] == 'GALX'):
                    self.input_galx = attrs[2][1]
            # instantiate the parser and fed it some HTML
        parser = MyHTMLParser()
        parser.feed(handle.read())
        params = {'dsh': parser.input_dsh, 'Email': cfg['ingress_login'], 'Passwd': cfg['ingress_pass'], 'GALX': parser.input_galx}
        settings.post_data = urllib.urlencode(params)
        try:
            req = http_request(settings.login_url, settings.post_data, settings.request_headers)
            handle = http_opener(req)
        except IOError, e:
            log.error('We failed to open "%s".' % settings.login_url)
            if hasattr(e, 'code'):
                log.error('We failed with error code - %s. ' % e.code, settings.login_url)
            elif hasattr(e, 'reason'):
                log.error('The error object has the following "reason" attribute :' + e.reason)
                log.error("This usually means the server doesn't exist, is down, or we don't have an internet connection.")
                sys.exit()
        handle.info()
        cookie_stor.save(cfg['cookie_file_path'])

    def get_ingress_last50_events(self):
        csrftoken = None
        for index, cookie in enumerate(cookie_stor):
            if cookie.name == 'csrftoken':
                csrftoken = cookie.value
        try:
            if csrftoken == None:
                raise Exception("csrftoken not assigned")
            log.debug("execute: get_ingress_last50_events")
            settings.post_data = '{"desiredNumItems":50,"minLatE6":52470756,"minLngE6":20578394,"maxLatE6":5240179,"maxLngE6":20761213,"minTimestampMs":-1,"maxTimestampMs":-1,"factionOnly":false,"method":"dashboard.getPaginatedPlextsV2"}'
            request_head = settings.request_headers
            request_head['Accept'] = 'application/json, text/javascript, */*; q=0.01'
            request_head['DNT'] = '1'
            request_head['Content-Type'] = 'application/json; charset=utf-8'
            request_head['X-Requested-With'] = 'XMLHttpRequest'
            request_head['Referer'] = 'http://www.ingress.com/intel'
            request_head['X-CSRFToken'] = csrftoken
            req = http_request(settings.chat_url, settings.post_data, request_head)
            handle = http_opener(req)
        except IOError, e:
            log.error('We failed to open "%s".' % settings.chat_url)
            if hasattr(e, 'code'):
                log.error('We failed with error code - %s. ' % e.code, settings.chat_url)
                raise
            elif hasattr(e, 'reason'):
                log.error('The error object has the following "reason" attribute :' + e.reason)
                log.error("This usually means the server doesn't exist, is down, or we don't have an internet connection.")
                sys.exit()
        else:
            return handle.read()

    def run(self):
        if cfg['use_gtalk'] == 1:
            notification.init_jabber()
        log.info('application started')
        try:
            while True:
                log.debug("parse started")
                start_time = time.time()
                try:
                    chat_json = self.get_ingress_last50_events()
                except:
                    log.error('Unexpected error:' + traceback.format_exc())
                    self.login_and_get_cookies()
                    chat_json = self.get_ingress_last50_events()
                    try:
                        chat_parser.parse_chat_to_db(chat_json)
                    except:
                        log.error('json:' + chat_json)
                        log.error('Unexpected error:' + traceback.format_exc())
                else:
                    try:
                        chat_parser.parse_chat_to_db(chat_json)
                    except:
                        log.error('json:' + chat_json)
                        log.error('Unexpected error:' + traceback.format_exc())
                log.debug("parse compleated")
                finish_time = time.time()
                sleep_timer = finish_time - start_time
                if sleep_timer > cfg['timeout']:
                    sleep_timer = 0
                else:
                    sleep_timer = cfg['timeout'] - sleep_timer
                log.info('Sleep: %s seconds' % int(sleep_timer))
                time.sleep(sleep_timer)
        finally:
            notification.close_jabber()
            log.info('application ended')
