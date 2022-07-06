#!/usr/bin/python
# Copyright (c) 2018 Warren Usui, MIT License
# pylint: disable=W0223
"""
Function used to extract html data to get season number
"""
from html.parser import HTMLParser
import requests
from ll_local_io import *
# print(HTMLParser)
# resp = requests.get("http://www.learnedleague.com")

# print(resp.text)

class GetSeasonNumber(HTMLParser):
    """
    Parse main page to get current season number
    """
    def __init__(self):
        HTMLParser.__init__(self)
        self.result = ''

    def handle_starttag(self, tag, attrs):
        """
        Find first href referring to standings.php
        """
        if tag == 'a':
            if attrs[0][0] == 'href':
                if attrs[0][1].startswith(STANDINGS):
                    if self.result == '':
                        tindx = attrs[0][1].find('?') + 1
                        self.result = attrs[0][1][tindx:]
                        if self.result.find('&') >= 0:
                            self.result = self.result[:self.result.find('&')]

def get_season(session=None):
    """
    Find the season number

    Input:
        session request

    Returns most recent season number
    """
    if session is None:
        session = get_session()
    return int(get_page_data(LLHEADER, GetSeasonNumber(), session=session))
