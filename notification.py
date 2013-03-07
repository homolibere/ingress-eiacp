__author__ = 'homolibere'

import smtplib
import sys
import sleekxmpp
import ssl
import traceback
import threading
import logging

import settings

from sleekxmpp.xmlstream import cert

if sys.version_info < (3, 0):
    from sleekxmpp.util.misc_ops import setdefaultencoding
    setdefaultencoding('utf8')
else:
    raw_input = input

xmpp = None
cfg = settings.load_config()

class mail_thread(threading.Thread):

    def __init__(self, mailto, mailbody):
        threading.Thread.__init__(self)
        self.mailto = mailto
        self.mailbody = mailbody

    def run(self):
        global cfg
        session = smtplib.SMTP(cfg['smtp_server'], cfg['smtp_port'])
        session.ehlo()
        session.starttls()
        session.ehlo()
        session.login(cfg['ingress_login'], cfg['ingress_pass'])
        session.sendmail(cfg['ingress_login'], self.mailto, self.mailbody)
        session.quit()

class GTalkBot(sleekxmpp.ClientXMPP):

    def __init__(self, jid, password):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)
        self.add_event_handler("ssl_invalid_cert", self.invalid_cert)

    def invalid_cert(self, pem_cert):
        der_cert = ssl.PEM_cert_to_DER_cert(pem_cert)
        try:
            cert.verify('talk.google.com', der_cert)
            print "CERT: Found GTalk certificate"
        except cert.CertificateError as err:
            print err.message, " : ", traceback.format_exc()
            self.disconnect(send_close=False)

    def start(self, event):
        self.send_presence()
        self.get_roster()

    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            msg.reply("I am a bot! I do not reply. Stop messaging me!").send()

def init_jabber():
    global xmpp
    global cfg
    xmpp = GTalkBot(cfg['ingress_login'], cfg['ingress_pass'])
    if xmpp.connect(('talk.google.com', 5222)):
        xmpp.process(block=False)
    else:
        print("Unable to connect jabber account.")

def close_jabber():
    global xmpp
    if xmpp <> None:
        xmpp.disconnect(send_close=True)

def send_reg_mail(mailto, nickname, passwd):
    global cfg
    headers = ["From: " + cfg['ingress_login'], "Subject: Registration Successful", "To: " + mailto, \
               "MIME-Version: 1.0", "Content-Type: text/html"]
    headers = "\r\n".join(headers)
    body = "\r\n\r\nHi, " + nickname + "! Congratulations and welcome!<br><br> Your login: <b>" + mailto + "</b> and password: <b>" + passwd + "</b>"
    body = headers + body
    mail_th = mail_thread(mailto, body)
    mail_th.start()
    send_jabber_invitation(mailto)

def send_mail_message(mailto, message):
    global cfg
    headers = ["From: " + cfg['ingress_login'], "Subject: Activity Detected", "To: " + mailto,\
               "MIME-Version: 1.0", "Content-Type: text/html"]
    headers = "\r\n".join(headers)
    body = "\r\n\r\n" + message
    body = headers + body
    mail_th = mail_thread(mailto, body)
    mail_th.start()
    send_jabber_invitation(mailto)

def send_jabber_message(sendto, message):
    global xmpp
    if xmpp <> None:
        xmpp.send_message(sendto, message)

def send_jabber_invitation(sendto):
    global xmpp
    if xmpp <> None:
        xmpp.send_presence(pto=sendto, ptype='subscribe')
        xmpp.send_presence_subscription(pto=sendto, ptype='subscribe', pnick='Ingress Notify Bot')
