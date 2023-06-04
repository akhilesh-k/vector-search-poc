import os
import requests
from tqdm import tqdm

def index_json_files(directory_path, solr_url, solr_username, solr_password):
    files = [file_name for file_name in os.listdir(directory_path) if file_name.endswith('.json')]
    total_files = len(files)

    for file_name in tqdm(files, total=total_files, desc='Indexing Files'):
        file_path = os.path.join(directory_path, file_name)
        with open(file_path, 'rb') as file:
            response = requests.post(
                solr_url,
                auth=(solr_username, solr_password),
                params={'commit': 'true'},
                headers={'Content-type': 'application/json'},
                data=file
            )
            if response.status_code == 200:
                tqdm.write(f"Indexed file: {file_name}")
            else:
                tqdm.write(f"Failed to index file: {file_name}")
                tqdm.write(f"Error message: {response.text}")

# Example usage
directory_path = '/Users/akhileshk/Search/vector_search_poc/data_encoder/data'
solr_url = 'http://localhost:8983/solr/retail-collection/update'
solr_username = 'solr'
solr_password = 'SolrRocks'

index_json_files(directory_path, solr_url, solr_username, solr_password)
