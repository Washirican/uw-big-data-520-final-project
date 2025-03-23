"""
Doc
"""

import json
import requests
from request_headers import HEADERS
from game_ids import GAME_IDs

def get_game_play_by_play(game_id):
    """
    Fetches the play-by-play data for a given NBA game.
    Parameters:
    game_id (str): The unique identifier for the NBA game.
    Returns:
    dict: A dictionary containing the raw play-by-play data if the request is successful.
    None: If the request fails, returns None and prints the status code.
    Raises:
    requests.exceptions.RequestException: If there is an issue with the HTTP request.
    """
    parameters = {'GameID': game_id,
                  'StartPeriod': 1,
                  'EndPeriod' : 4,
                  }

    endpoint = 'playbyplayv3'
    request_url = f'https://stats.nba.com/stats/{endpoint}?'

    response = requests.get(request_url, headers=HEADERS, params=parameters, timeout=10)

    if response.status_code == 200:
        raw_data = response.json()
        return raw_data
    else:
        print(f"Failed to get data: {response.status_code}")
        return None

def save_data_to_file(data, filename):
    """
    Save the given data to a file in JSON format.

    Parameters:
    data (dict): The data to be saved.
    filename (str): The name of the file where the data will be saved.

    Returns:
    None
    """
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def main():
    """
    Main function to retrieve and save game play-by-play data.
    This function retrieves the play-by-play data for a specified game ID
    and saves it to a JSON file. If no data is retrieved, it prints a message
    indicating that there is no data to save.
    Example:
        game_id = "0022401014"  # Replace with actual game ID
    """

    for idx, game_id in enumerate(GAME_IDs):
        data = get_game_play_by_play(game_id)

        if data:
            save_data_to_file(data, f"./game-play-by-play-data/game_play_by_play_data_{game_id}.json")
            print("Data saved successfully.")
        else:
            print("No data to save.")

if __name__ == "__main__":
    main()
