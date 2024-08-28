import os
import json

# Define the directory containing your JSON files
directory_path = '/path/to/your/json/files'

# List to store the data
data_list = []

# Iterate over each file in the directory
for filename in os.listdir(directory_path):
    if filename.endswith('.json'):  # Check if the file is a JSON file
        file_path = os.path.join(directory_path, filename)
        with open(file_path, 'r') as file:
            data = json.load(file)
            # Extract data from each specified test if they exist in the file
            orphans_result = data.get('tests', {}).get('test_find_orphans', {}).get('result', 'N/A')
            deadends_result = data.get('tests', {}).get('test_find_deadends', {}).get('result', 'N/A')
            orphans_count = data.get('tests', {}).get('test_find_orphans', {}).get('data', {}).get('count', 'N/A')
            deadends_count = data.get('tests', {}).get('test_find_deadends', {}).get('data', {}).get('count', 'N/A')
            
            # Append the results to the list
            data_list.append({
                'File ID': filename,
                'Test': 'test_find_orphans',
                'Result': orphans_result,
                'Orphan Metabolites Count': orphans_count
            })
            data_list.append({
                'File ID': filename,
                'Test': 'test_find_deadends',
                'Result': deadends_result,
                'Dead-end Metabolites Count': deadends_count
            })

# Output the results
for entry in data_list:
    print(entry)

