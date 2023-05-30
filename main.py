import pandas as pd
import requests


def get_players(league_id):
    url = "https://fantasy.premierleague.com/api/leagues-classic/{0}/standings/".format(league_id)
    print("Calling {}".format(url))
    return pd.DataFrame(requests.get(url).json()["standings"]["results"])

def get_gw_result(gw, team_id):
    url = "https://fantasy.premierleague.com/api/entry/{0}/event/{1}/picks/".format(team_id, gw)
    print("Calling {}".format(url))
    return requests.get(url).json()["entry_history"]


#league_id = 83736
league_id = 881782

players = get_players(league_id)
gw_results = []
for team_id in players['entry'].tolist():
    for gw in range(1, 39):
        try:
            res = get_gw_result(gw, team_id)
            res['entry'] = team_id
            gw_results.append(res)
        except:
            print("Something went wrong for {0} {1}".format( key, i))

gw_results_df = pd.DataFrame(gw_results)

combined_df = pd.merge(gw_results_df, players, on=["entry"])

combined_df[["entry","player_name","entry_name","event", "points", "overall_rank", "bank", "value", "event_transfers_cost", "points_on_bench"]].to_csv("combined.csv")

