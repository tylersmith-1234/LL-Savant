# required packages
import configparser
import requests
import json
import pickle
import pandas as pd

with open('pp_by_username.json', 'r') as fp:
    by_username = json.load(fp)
with open('player_profiles.json', 'r') as fp:
    player_profiles = json.load(fp)
undo_username_chg = {
    'obrien': 'o\'brien',
    'orourkek': 'o\'rourkek',
    'olearyn': 'o\'learyn',
    'o_brienm': 'o\'brienm',
    'o_brienp': 'o\'brienp',
    'o_neillj': 'o\'neillj',
    'vaidman_stonem': 'vaidman stonem',
    'zeidlere_bang_a_gong': 'zeidlere bang_a_gong',
    'johnsonnickoclock': 'johnsonnicko\'clock',
    'goedels_incompleteness': 'goedel\'s incompleteness',
    'frankly_my_dear_i_dont': 'frankly my dear i don\'t',
    'int_veldt': 'in\'t veldt',
    'rudenskyyes_its_me': 'rudenskyyes it\'s me',
    'frisciap_child_please': 'frisciap child_please',
    'trivedid_ancient_history': 'trivedid_ancient history'
}

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

def save_json_as_csv(season):
    with open(f'./FULL_DATA/LL{season}/results.json') as fp:
        cur = json.load(fp)
    matches_history, match_participation, player_answer_history = [], [], []
    for md_rundle in cur:
        matches_history.extend(md_rundle['matches_history'])
        match_participation.extend(md_rundle['match_participation'])
        player_answer_history.extend(md_rundle['player_answer_history'])
    matches_history = pd.DataFrame(matches_history,
        columns=['match_id', 'rundle', 'league', 'div', 'season', 'md'])
    match_participation = pd.DataFrame(match_participation,
        columns=['match_id', 'season', 'md', 'rundle', 'league', 'div', 'player', 'result'])
    match_participation['player'] = match_participation['player'].str.lower()
    player_answer_history = pd.DataFrame(player_answer_history,
        columns=['match_id', 'rundle', 'league', 'div', 'season', 'md', 'qnum', 'player', 'correct', 'def_given'])
    player_answer_history['player'] = player_answer_history['player'].str.lower()
    match_participation['player_id'] = match_participation.apply(username_to_id, axis=1)
    player_answer_history['player_id'] = player_answer_history.apply(username_to_id, axis=1)
    matches_history.to_csv(f'./FULL_DATA/LL{season}/matches_history.csv')
    match_participation.to_csv(f'./FULL_DATA/LL{season}/match_participation.csv')
    player_answer_history.to_csv(f'./FULL_DATA/LL{season}/player_answer_history.csv')
    print(f'complete resaving of LL{season}')

def username_to_id(row):
    global by_username
    u = str(row['player']).strip()
    if u.isnumeric(): return u
    elif u in undo_username_chg.keys(): u = undo_username_chg[u]
    if u not in by_username.keys() and '_' in u: u = u.replace('_', ' ')
    if u not in by_username.keys() and u[0] in ['o', 'd']: u = f'{u[0]}\'{u[1:]}'
    if u not in by_username.keys():
        id = add_id_to_dicts(u)
        with open('pp_by_username.json', 'r') as fp:
            by_username = json.load(fp)
    #     return str(id)
    return by_username[u]

def add_id_to_dicts(new_id: str):
    new_p = build_base_player(new_id.replace('\' ', '_').replace(' ', '_'))
    with open('player_profiles.json', 'r') as fp:
        player_profiles = json.load(fp)
    with open('pp_by_username.json', 'r') as fp:
        by_username = json.load(fp)
    player_profiles[str(new_p['id'])] = new_p
    # print(new_p)
    by_username[new_p['name'].lower() if 'name' in new_p.keys() else new_p['username'].lower()] = str(new_p['id'])
    with open('player_profiles.json', 'w') as fp:
        json.dump(player_profiles, fp)
    with open('pp_by_username.json', 'w') as fp:
        json.dump(by_username, fp)
    return new_p['id']