# required packages
import configparser
import requests
import json
import pickle

def get_session(force_new_session=False):
    """
    Read an ini file, establish a login session

    Input:
        inifile -- name of local ini file with control information

    Returns: logged in requests session to be used in later operations
    """
    if not force_new_session:
        try:
            with open('session.pkl', 'rb') as f:
                ses1 = pickle.load(f)
            print('using existing login session')
        except:
            ses1 = requests.Session()
            print('creating new login session...')
    else:
        ses1 = requests.Session()
        print('creating new login session...')
    config = configparser.ConfigParser()
    with open('constants.json', 'r') as d:
        constants = json.load(d)
    config.read(constants['INPUTDATA']) # reads a file with name 'logindata.ini' (see constants.json). That file should have format:
    """
[DEFAULT]
username = {your username here without braces}
password = {your password here without braces}
    """
    payload = {'login': 'Login'}
    for attrib in ['username', 'password']:
        payload[attrib] = config['DEFAULT'][attrib]
    try:
        loginfile = config['DEFAULT']['loginfile']
    except KeyError:
        loginfile = constants['LOGINFILE']
    ses1.post(loginfile, data=payload)
    with open('session.pkl', 'wb') as f:
        pickle.dump(ses1, f)
    return ses1

def int_or_float_or_str(s: str):
    try:
        try:
            return int(s)
        except ValueError:
            return float(s)
    except ValueError:
        return str(s)