import requests
import json

def get_team_id(team_name, dataset_path="dataset/allteams.json"):
    with open(dataset_path, "r", encoding="utf-8") as f:
        teams = json.load(f)
    
    for team in teams:
        if team["name"].lower() == team_name.lower():
            return team["id"]
    
    return None

def get_upcoming_match(team1, team2):
    response = requests.get("https://5000-krushna06-statsvlrapi-gwwjqnmwcoo.ws-us118.gitpod.io/api/v1/matches")
    
    if response.status_code != 200:
        print("Error fetching match data.")
        return None
    
    matches = response.json().get("data", [])
    
    for match in matches:
        teams = [team["name"].lower() for team in match["teams"]]
        if team1.lower() in teams and team2.lower() in teams:
            return match
    
    return None

def get_match_history(team_id):
    url = f"https://5000-krushna06-statsvlrapi-gwwjqnmwcoo.ws-us118.gitpod.io/api/v1/match-history?team={team_id}"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error fetching match history for team ID {team_id}.")
        return None

    try:
        data = response.json().get("data", [])
        return data
    except json.JSONDecodeError:
        print(f"Failed to parse JSON for team {team_id}: {response.text}")
        return None

def filter_head_to_head_matches(team1, team2, match_history):
    return [match for match in match_history if 
            any(team1.lower() == t["name"].lower() for t in match["teams"]) and
            any(team2.lower() == t["name"].lower() for t in match["teams"])]

def calculate_recent_form(matches, recent_games=5):
    recent_matches = matches[:recent_games]
    wins = sum(1 for match in recent_matches if match["teams"][0]["score"] > match["teams"][1]["score"])
    return wins / len(recent_matches) if recent_matches else 0, recent_matches

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
    
    head_to_head = filter_head_to_head_matches(team1, team2, team1_history)
    head_to_head_wins = sum(1 for match in head_to_head if match["teams"][0]["score"] > match["teams"][1]["score"])
    head_to_head_total = len(head_to_head)
    head_to_head_win_rate = head_to_head_wins / head_to_head_total if head_to_head_total > 0 else 0

    team1_recent_form, team1_recent_matches = calculate_recent_form(team1_history)
    team2_recent_form, team2_recent_matches = calculate_recent_form(team2_history)

    print("\n-- Prediction Breakdown --")

    print(f"\n{team1} Recent Matches Considered: {len(team1_recent_matches)}")
    for match in team1_recent_matches:
        opponent = [t["name"] for t in match["teams"] if t["name"] != team1][0]
        score = f'{match["teams"][0]["score"]}-{match["teams"][1]["score"]}'
        print(f"   vs {opponent}: {score}")
    
    print(f"{team1} Recent Win Rate: {team1_recent_form:.2f}")

    print(f"\n{team2} Recent Matches Considered: {len(team2_recent_matches)}")
    for match in team2_recent_matches:
        opponent = [t["name"] for t in match["teams"] if t["name"] != team2][0]
        score = f'{match["teams"][0]["score"]}-{match["teams"][1]["score"]}'
        print(f"   vs {opponent}: {score}")

    print(f"{team2} Recent Win Rate: {team2_recent_form:.2f}")

    print(f"\n{team1} vs {team2} Head-to-Head Matches Considered: {head_to_head_total}")
    for match in head_to_head:
        score = f'{match["teams"][0]["score"]}-{match["teams"][1]["score"]}'
        print(f"   {team1} vs {team2}: {score}")

    print(f"{team1} Head-to-Head Win Rate: {head_to_head_win_rate:.2f}")
    print(f"{team2} Head-to-Head Win Rate: {1 - head_to_head_win_rate:.2f}")

    weight_recent = 0.6
    weight_head_to_head = 0.4

    team1_score = (team1_recent_form * weight_recent) + (head_to_head_win_rate * weight_head_to_head)
    team2_score = (team2_recent_form * weight_recent) + ((1 - head_to_head_win_rate) * weight_head_to_head)

    predicted_winner = team1 if team1_score > team2_score else team2
    print(f"\nPredicted Winner: {predicted_winner}")

if __name__ == "__main__":
    team1 = input("Enter Team 1 Name: ")
    team2 = input("Enter Team 2 Name: ")
    predict_winner(team1, team2)
