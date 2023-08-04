import requests
import json
import signal
from dotenv import dotenv_values

# Load environment variables from the file
env_vars = dotenv_values('config.env')
print(env_vars)

# Access the URL from the environment variables
url = env_vars.get('SOLR_URL')

if url is None:
    print("Error: SOLR_URL environment variable is not set.")
    exit(1)

# Number of objects to write in each file
objects_per_file = 5000


# Interrupt signal handler
def interrupt_handler(signal, frame):
    print("\nKeyboard interrupt detected. Saving the current result as solr_result.json.")
    write_result(result)
    exit(0)


# Register interrupt signal handler
signal.signal(signal.SIGINT, interrupt_handler)

# Send GET request to Solr
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()  # Parse the response as JSON
    # Total number of documents available
    num_found = data['response']['numFound']
    # Number of documents per page
    rows = data['responseHeader']['params']['rows']
    start = 0  # Start index for pagination
    result = []  # List to store all the documents
    file_number = 1  # Initial file number

    # Function to write the result list to a JSON file

    def write_result(result, filename="solr_result.json"):
        with open(filename, 'w') as file:
            json.dump(result, file)

    try:
        while start < num_found:
            # Update the start parameter in the URL for pagination
            paginated_url = url + "&start=" + str(start)

            # Send paginated request to Solr
            paginated_response = requests.get(paginated_url)

            # Check if the paginated request was successful
            if paginated_response.status_code == 200:
                # Parse the paginated response as JSON
                paginated_data = paginated_response.json()
                # List of documents in the current page
                docs = paginated_data['response']['docs']
                result.extend(docs)  # Append the documents to the result list

                # Check if the result list has reached the objects_per_file limit
                if len(result) >= objects_per_file:
                    # Write the result list to a file
                    filename = f"data-{file_number}.json"
                    write_result(result, filename)
                    file_number += 1
                    result = []  # Reset the result list
            else:
                print("Error in paginated request:",
                      paginated_response.status_code)
                break

            start += int(rows)  # Update the start index for the next page
    except KeyboardInterrupt:
        # Keyboard interrupt (Ctrl+C) detected
        print(
            "\nKeyboard interrupt detected. Saving the current result as solr_result.json.")
        write_result(result)
        exit(0)

    # Write the remaining result list to a file
    if len(result) > 0:
        filename = f"data-{file_number}.json"
        write_result(result, filename)

    print("Export complete. Total documents:", num_found)
else:
    print("Error in Solr request:", response.status_code)
