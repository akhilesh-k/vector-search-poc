import os
import json

def find_missing_nameSearch(directory_path):
    for file_name in os.listdir(directory_path):
        if file_name.endswith('.json'):
            file_path = os.path.join(directory_path, file_name)
            with open(file_path, 'r') as file:
                try:
                    json_data = json.load(file)
                    for obj in json_data:
                        if 'merchantName' not in obj:
                            print(f"File: {file_name}, id: {obj['id']}")
                except json.JSONDecodeError:
                    print(f"Error reading JSON data from file: {file_name}")

# Example usage
directory_path = '../data'
find_missing_nameSearch(directory_path)
