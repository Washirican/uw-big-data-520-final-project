import json
import requests
from request_headers import HEADERS
from game_ids import GAME_IDs


def get_game_box_score(game_id):
    """
    Fetches the box score summary for a given NBA game.
    Parameters:
    game_id (str): The unique identifier for the NBA game.
    Returns:
    dict: A dictionary containing the raw JSON data of the box score summary
    if the request is successful.
    None: If the request fails, returns None and prints the status code.
    Raises:
    requests.exceptions.RequestException: If there is an issue with the
    HTTP request.
    """
    parameters = {'GameID': game_id}

    endpoint = 'boxscoresummaryv2'
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

    Args:
        data (dict): The data to be saved.
        filename (str): The name of the file where the data will be saved.

    Returns:
        None
    """
    with open(filename, 'w', encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def main():
    """
    Main function to retrieve and save the box score data for a specified
    .
    This function uses a predefined game ID to fetch the box score data
    using the
    `get_game_box_score` function. If data is successfully retrieved, it
    saves the
    data to a JSON file named "get_game_box_score_data.json". If no data
    is retrieved,
    it prints a message indicating that there is no data to save.
    Note:
        Replace the example game ID with the actual game ID as needed.
    Returns:
        None
    """

    for idx, game_id in enumerate(GAME_IDs):
        data = get_game_box_score(game_id)

        if data:
            save_data_to_file(data, f"./box-score-data/box_score_data_{game_id}.json")
            print(f"Data for game_id {game_id} saved successfully.")
        else:
            print("No data to save.")

if __name__ == "__main__":
    main()
