
import json
import requests
from request_headers import HEADERS
import csv


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


player_index_url = 'https://stats.nba.com/js/data/ptsd/stats_ptsd.js'
player_list = requests.get(player_index_url)

# Cleanup string
dict_str = player_list.content.decode()[17:-1]

# Turns string into dictionary
data = json.loads(dict_str)
players = data['data']['players']
teams = data['data']['teams']
data_date = data['generated']

# Save player list as csv file
csv_file_path = "./active_player_list/active_players.csv"

# Open the CSV file for writing
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write the header row
    csv_writer.writerow(['player_id', 'player_name', 'team'])

    # Write player data rows
    for player in players:
        if player[-1] != '':
            player_id = player[0]
            name = player[1].split(', ')[1] + ' ' + player[1].split(', ')[0]
            team = player[-1].title()
            csv_writer.writerow([player_id, name, team])


