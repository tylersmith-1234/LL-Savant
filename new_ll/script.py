"""
Handle Local I/O and global definitions

INPUTDATA (logindata.ini) is a local file that controls what happens here.

In the DEFAULT section of INPUTDATA, the following must be defined:
    username -- a valid LL name
    password -- the LL password corresponding to username
"""
from bs4 import BeautifulSoup
import configparser
from requests import session
import requests

LLHEADER = 'https://www.learnedleague.com'
LOGINFILE = LLHEADER + '/ucp.php?mode=login'
USER_DATA = LLHEADER + '/profiles/previous.php?%s'
QHIST = LLHEADER + '/profiles/qhist.php?%s'
MATCH_DATA = LLHEADER + '/match.php?%s'
ONEDAYS = LLHEADER + '/oneday'
STANDINGS = '/standings.php?'
LLSTANDINGS = LLHEADER + STANDINGS
ARUNDLE = LLSTANDINGS + '%d&A_%s'
INPUTDATA = 'logindata.ini'
TOTAL_MATCHES_PER_SEASON = 25

class Question:
    def __init__(self, text, season, day, qnum, correct) -> None:
        self.text = text
        self.season = season
        self.day = day
        self.qnum = qnum
        self.correct = correct
print(Question)
# def get_session():
#     """
#     Read an ini file, establish a login session

#     Input:
#         inifile -- name of local ini file with control information

#     Returns: logged in requests session to be used in later operations
#     """
#     config = configparser.ConfigParser()
#     config.read(INPUTDATA)
#     payload = {'login': 'Login'}
#     for attrib in ['username', 'password']:
#         payload[attrib] = config['DEFAULT'][attrib]
#     ses1 = requests.Session()
#     try:
#         loginfile = config['DEFAULT']['loginfile']
#     except KeyError:
#         loginfile = LOGINFILE
#     ses1.post(loginfile, data=payload)
#     return ses1
# # get_session()
# # main_data = sess.get(LLHEADER)
# # html_text = main_data.text
# # soup = BeautifulSoup(html_text, 'html.parser')
# # print(soup)
# # parser1 = parser
# # parser1.feed(main_data.text)
# # return parser1.result
# with session() as c:
#     # c.post(LLHEADER, data={'login': "Login", 'username': '<USER>', 'password': '<PASS>'})
#     req = c.get(LLHEADER)
#     html_text = req.text
#     # print(req.headers)
#     # print(req.text)
#     # html_text = c.get(LLHEADER).text
#     soup = BeautifulSoup(html_text, 'html.parser')
#     print(soup)
#     c.close()
#     req.close()