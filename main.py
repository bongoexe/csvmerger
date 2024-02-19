import csv
import glob
import os
import sys
import time
from tqdm import tqdm  # Import the tqdm function

# Try to set the maximum size of fields.
csv.field_size_limit(sys.maxsize)

input_directory_path = 'path'
output_csv_file_path = 'path'

csv_files = glob.glob(os.path.join(input_directory_path, '*.csv'))

with open(output_csv_file_path, 'w', newline='', encoding='utf-8') as output_file:
    csv_writer = csv.writer(output_file)
    
    header_written = False
    
    # Wrap the file processing loop with tqdm for a progress bar
    for file_path in tqdm(csv_files, desc="Processing files"):
        file_opened = False
        while not file_opened:
            try:
                with open(file_path, 'r', newline='', encoding='utf-8') as input_file:
                    file_opened = True  # File successfully opened
                    csv_reader = csv.reader((line.replace('\0', '') for line in input_file))
                    header = next(csv_reader, None)
                    
                    if not header_written and header:
                        csv_writer.writerow(header)
                        header_written = True
                        
                    if header:
                        for row in csv_reader:
                            try:
                                csv_writer.writerow(row)
                            except csv.Error as e:
                                print(f'Error processing line in {file_path}: {e}. Line was skipped.')
            except FileNotFoundError:
                print(f'File {file_path} not found. Waiting for 1 minute before retrying.')
                time.sleep(60)  # Wait for 1 minute before retrying
            except Exception as e:
                print(f'An unexpected error occurred with {file_path}: {e}. Skipping this file.')
                break  # Exit the while loop if an error other than FileNotFoundError occurs

print('CSV merging process completed. Check output for any skipped lines.')
