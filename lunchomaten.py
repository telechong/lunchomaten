#
#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  <jonas@agilefrog.se> wrote this file. As long as you retain this notice you
#  can do whatever you want with this stuff. If we meet some day, and you think
#  this stuff is worth it, you can buy me a beer in return Jonas Ericsson
#  ----------------------------------------------------------------------------
#

#!/usr/bin/env python

import time
import random
import smtplib
from email.mime.text import MIMEText
from ConfigParser import ConfigParser
import pycron


def main():
    config = ConfigParser()
    config.readfp(open('lunchomaten.cfg'))
    restaurants = get_restaurants()
    selection = make_selection(restaurants)
    print "Today we eat at %s" % selection
    send_mail(selection, config)


def get_restaurants():
    data = open('restaurants.txt')
    restaurants = []
    for line in data:
        restaurants.append(line)
    return restaurants


def make_selection(restaurants):
    return random.sample(restaurants, 1)


def send_mail(selection, config):
    message = MIMEText('Today we eat at %s' % selection)
    message['To'] = config.get('mail', 'to')
    message['From'] = config.get('mail', 'from')
    message['Subject'] = 'Lunch time!'

    server = smtplib.SMTP(config.get('mail', 'server'))
    server.sendmail('Lunchomaten', config.get('mail', 'to'),
            message.as_string())
    server.quit()


if __name__ == '__main__':
    cron = pycron.pycron()
    cron.add_job('1 5 5 * * 1-5', main, 'main job')
    while True:
        time.sleep(1)
        for match in cron.get_matched_jobs():
            match()
