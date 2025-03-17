import requests
import json

def get_team_id(team_name, dataset_path="dataset/allteams.json"):
    try:
        with open(dataset_path, "r", encoding="utf-8") as f:
            teams = json.load(f)
        
        for team in teams:
            if team["name"].lower() == team_name.lower():
                return team["id"]
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading team dataset: {e}")
    
    return None

def get_upcoming_match(team1, team2):
    url = "https://5000-krushna06-statsvlrapi-gwwjqnmwcoo.ws-us118.gitpod.io/api/v1/matches"
    response = requests.get(url)

    if response.status_code != 200:
        print("Error fetching match data.")
        return None

    try:
        matches = response.json().get("data", [])
        for match in matches:
            teams = [team["name"].lower() for team in match["teams"]]
            if team1.lower() in teams and team2.lower() in teams:
                return match
    except json.JSONDecodeError:
        print("Failed to parse match data.")
    
    return None

def get_match_history(team_id):
    url = f"https://5000-krushna06-statsvlrapi-gwwjqnmwcoo.ws-us118.gitpod.io/api/v1/match-history?team={team_id}"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error fetching match history for team ID {team_id}.")
        return None

    try:
        data = response.json()
        if "data" not in data or not isinstance(data["data"], list):
            print(f"Unexpected response format for team {team_id}: {data}")
            return None
        return data["data"]
    except json.JSONDecodeError:
        print(f"Failed to parse JSON for team {team_id}: {response.text}")
        return None

def predict_winner(team1, team2):
    team1_id = get_team_id(team1)
    team2_id = get_team_id(team2)
    
    if not team1_id or not team2_id:
        print("One or both team names are invalid.")
        return
    
    match = get_upcoming_match(team1, team2)
    if not match:
        print("No upcoming match found.")
        return
    
    team1_history = get_match_history(team1_id)
    team2_history = get_match_history(team2_id)
    
    if not team1_history or not team2_history:
        print("Error retrieving match histories.")
        return
    
    def count_wins(team_name, history):
        wins = 0
        for match in history:
            teams = {}
            for t in match["teams"]:
                try:
                    teams[t["name"]] = int(t["score"]) if t["score"].isdigit() else 0
                except ValueError:
                    teams[t["name"]] = 0
            
            if team_name in teams:
                team_score = teams[team_name]
                opponent_score = max(score for t, score in teams.items() if t != team_name)
                if team_score > opponent_score:
                    wins += 1
        return wins

    team1_wins = count_wins(team1, team1_history)
    team2_wins = count_wins(team2, team2_history)

    total_team1_matches = len(team1_history)
    total_team2_matches = len(team2_history)

    team1_win_rate = team1_wins / total_team1_matches if total_team1_matches > 0 else 0
    team2_win_rate = team2_wins / total_team2_matches if total_team2_matches > 0 else 0

    print("\n--- Match History Analysis ---")
    print(f"{team1}: {team1_wins} Wins / {total_team1_matches} Matches | Win Rate: {team1_win_rate:.2%}")
    print(f"{team2}: {team2_wins} Wins / {total_team2_matches} Matches | Win Rate: {team2_win_rate:.2%}")

    predicted_winner = team1 if team1_win_rate > team2_win_rate else team2
    print(f"\n🎯 Predicted Winner: {predicted_winner} 🎯")

if __name__ == "__main__":
    team1 = input("Enter Team 1 Name: ")
    team2 = input("Enter Team 2 Name: ")
    predict_winner(team1, team2)
