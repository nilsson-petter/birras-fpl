import pandas as pd
import requests


def get_teams_in_league(league_id):
    url = "https://fantasy.premierleague.com/api/leagues-classic/{0}/standings/".format(league_id)
    print("Calling {}".format(url))
    return pd.DataFrame(requests.get(url).json()["standings"]["results"])

def get_gw_result(gw, team_id):
    url = "https://fantasy.premierleague.com/api/entry/{0}/event/{1}/picks/".format(team_id, gw)
    print("Calling {}".format(url))
    return requests.get(url).json()["entry_history"]


league_id = 80816

teams = get_teams_in_league(league_id)
gw_results = []
for team_id in teams['entry'].tolist():
    for gw in range(1, 13):
        try:
            res = get_gw_result(gw, team_id)
            res['entry'] = team_id
            gw_results.append(res)
        except:
            print("Something went wrong for {0} {1}".format(team_id, gw))

gw_results_df = pd.DataFrame(gw_results)

combined_df = pd.merge(gw_results_df, teams, on=["entry"])

combined_df[["entry","player_name","entry_name","event", "points", "overall_rank", "bank", "value", "event_transfers_cost", "points_on_bench"]].to_csv("combined.csv")

