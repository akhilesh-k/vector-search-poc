import os
import json

def remove_version_field(json_data):
    for obj in json_data:
        obj.pop('_version_', None)

def find_missing_nameSearch(directory_path):
    for file_name in os.listdir(directory_path):
        if file_name.endswith('.json'):
            file_path = os.path.join(directory_path, file_name)
            with open(file_path, 'r+') as file:
                try:
                    json_data = json.load(file)
                    remove_version_field(json_data)
                    file.seek(0)  # Move the file pointer to the beginning
                    json.dump(json_data, file, indent=4)
                    file.truncate()  # Truncate the remaining content
                    for obj in json_data:
                        if 'merchantName' not in obj:
                            print(f"File: {file_name}, id: {obj['id']}")
                except json.JSONDecodeError:
                    print(f"Error reading JSON data from file: {file_name}")

# Example usage
directory_path = '/Users/akhileshk/Search/vector_search_poc/data_encoder/data'
find_missing_nameSearch(directory_path)
