import json
import requests
from request_headers import HEADERS
from bs4 import BeautifulSoup

HEADERS = {
        'Host': 'stats.nba.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) '
                      'Gecko/20100101 Firefox/72.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'x-nba-stats-origin': 'stats',
        'x-nba-stats-token': 'true',
        'Connection': 'keep-alive',
        'Referer': 'https://www.nba.com/',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        }


# TODO (2025-03-22): Fix code to get game list by date

def get_nba_games_by_date(date):
    """
    Get all NBA games and scores from a given date.

    Parameters:
    date (str): The date in the format 'YYYY-MM-DD'.

    Returns:
    list: A list of dictionaries containing game information.
    """
    url = f"https://www.nba.com/games?date={date}"
    url = "https://core-api.nba.com/cp/api/v1.9/feeds/gamecardfeed?gamedate=03/22/2025&platform=web"

    response = requests.get(url, headers=HEADERS) # , timeout=10)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        games = []

        for game in soup.find_all('div', class_='GameCard_gc__UCI46 GameCardsMapper_gamecard__pz1rg'):
            home_team = game.find('div', class_='TeamLogo_logo__3pT9z').text.strip()
            visitor_team = game.find('div', class_='TeamLogo_logo__3pT9z').text.strip()
            home_team_score = game.find('div', class_='TeamScore_score__2r5xD').text.strip()
            visitor_team_score = game.find('div', class_='TeamScore_score__2r5xD').text.strip()

            games.append({
                'home_team': {'full_name': home_team},
                'visitor_team': {'full_name': visitor_team},
                'home_team_score': home_team_score,
                'visitor_team_score': visitor_team_score
            })

        return games
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return []

# Example usage
date = "2025-03-21"
games = get_nba_games_by_date(date)
for game in games:
    print(f"{game['home_team']['full_name']} vs {game['visitor_team']['full_name']}: {game['home_team_score']} - {game['visitor_team_score']}")