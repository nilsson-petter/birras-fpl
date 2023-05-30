import pandas as pd
import requests


def get_players(league_id):
    url = "https://fantasy.premierleague.com/api/leagues-classic/{0}/standings/".format(league_id)
    print("Calling {}".format(url))
    r = requests.get(url)
    json = r.json()
    result = dict()
    return pd.DataFrame(json['standings']['results'])

def get_gw_result(gw, team_id):
    url = "https://fantasy.premierleague.com/api/entry/{0}/event/{1}/picks/".format(team_id, gw)
    print("Calling {}".format(url))
    r = requests.get(url)
    json = r.json()
    return json['entry_history']


league_id = 83736

players = get_players(league_id)
gw_results = []
for key in players['entry'].tolist():
    for i in range(1, 39):
        try:
            #Exclude cancelled GW 7
            if i != 7:
                res = get_gw_result(i, key)
                res['entry'] = key
                gw_results.append(res)
        except:
            print("Something went wrong for {0} {1}", key, i)

gw_results_df = pd.DataFrame(gw_results)

combined_df = pd.merge(gw_results_df, players, on=["entry"])

combined_df[["entry","player_name","entry_name","event", "points", "overall_rank", "bank", "value", "event_transfers_cost", "points_on_bench"]].to_csv("combined.csv")

