import csv
import random

def select_random_players(file_path, num_records=3):
    """
    Randomly selects a specified number of records from a CSV file.

    :param file_path: Path to the CSV file containing player data.
    :param num_records: Number of records to randomly select.
    :return: List of randomly selected records.
    """
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = list(csv.DictReader(csvfile))
            if len(reader) < num_records:
                raise ValueError("The file contains fewer records than requested.")
            return random.sample(reader, num_records)
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except ValueError as e:
        print(f"Error: {e}")

# Example usage
if __name__ == "__main__":
    file_path = "./active-player-list/active_players.csv"
    selected_players = select_random_players(file_path)
    if selected_players:
        for player in selected_players:
            print(player)