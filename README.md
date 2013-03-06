# Introduction

This project is a extension to Google's game - Ingress. Since there is no official API for this game (so far) and no other way to get more info about players and portals, i decided to create a python "daemon".

We are currently developing Web UI for tgis daemon, so stay tuned.

# Features (what we can get from ingress chat?)

when and where player:
* deployed a resonator
* destroyed a resonator
* created a link
* destroyed a link
* created a field
* destroyed a field
* field decation
* portal mods decation
* player level - based on level of deployed resonator
* notification to any jabber or e-mail about actions (player actions, actions to portal)

All this data stored in MySQL database and you can use it to create:
* heat map of player activity
* heat map of faction activity
* statistics (symmary or daily/monthly)

# Installation & Running

Python 2.7.x required.

First of all we need preinstall dependencies, such as:
* PyMySQL
* sleekxmpp
* pyasn1 (optional)
* pyasn1_modules (optional)

then you just need to change dir to where you put source

For Linux based (this will start a daemon - kind of ;) ):
cd /path/to/ingress-eiacp/dir
python __init__.py start

For Other (this will start an application in window):
cd /path/to/ingress-eiacp/dir
python __init__.py


btw grant write permissions to this dir (it's for writing log - stdout.log)