#!/usr/bin/env python
# -*- coding: utf-8 -*-

from requests_oauthlib import OAuth1Session
from xml.etree import ElementTree as ET 
from datetime import date 
import urllib2
import os
from string import Template
import sys

env = os.environ

github_contributions_url = Template('https://github.com/users/${GITHUB_USERNAME}/contributions').substitute(GITHUB_USERNAME = env.get('GITHUB_USERNAME'))

response = urllib2.urlopen(github_contributions_url)
html = response.read()

elements = ET.XML(html)

rect_list = []

for element in elements.iter("rect"):
    rect_list.append(element)

act_list = []

for element in rect_list:
    if int(element.get("data-count")) > 0:
        act_list.append(element)

act_strdate_list = []

for element in act_list:
    act_strdate_list.append(element.get("data-date"))


def formatStringToDate(str):
    a = str.split("-")
    return date(int(a[0]),int(a[1]),int(a[2]))

act_date_list = []

for element in act_strdate_list:
    a = formatStringToDate(element)
    act_date_list.append(a)

sorted_list = sorted(act_date_list)

last_commited_date = sorted_list[-1]

today = date.today()

days_ago = (today - last_commited_date).days

message_1 = ""

if days_ago == 0:
    message_1 = "It\'s just today"
elif days_ago == 1:
    message_1 = "It\'s yesterday"
else:
    message_1 = "It\'s " + str(days_ago) + "days"

message_2 = Template(" that I last pushed to GitHub. \n\
https://github.com/${GITHUB_USERNAME}").substitute(GITHUB_USERNAME = env.get('GITHUB_USERNAME'))

message = message_1 + message_2


CK = env.get('CONSUMER_KEY') 
CS = env.get('CONSUMER_SECRET')
AT = env.get('ACCESS_TOKEN')
AS = env.get('ACCESS_TOKEN_SECRET')

url = "https://api.twitter.com/1.1/statuses/update.json"

params = {"status": message}

twitter = OAuth1Session(CK, CS, AT, AS)
req = twitter.post(url, params = params)

if req.status_code == 200:
    print ("OK")
    sys.exit(0)
else:
    sys.exit("Error: %d" % req.status_code)
    
