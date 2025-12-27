import csv
import os
import tempfile

file_path = os.path.join('output', 'output.csv')

# Create a temporary file in the same directory
temp_fd, temp_path = tempfile.mkstemp(dir=os.path.dirname(file_path))

seen = set()

with open(file_path, 'r', newline='', encoding='utf-8') as infile, \
     open(temp_path, 'w', newline='', encoding='utf-8') as outfile:

    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        key = tuple(row[f] for f in fieldnames)
        if key in seen:
            print('Duplicate row:', row)
        else:
            seen.add(key)
            writer.writerow(row)

# Close and remove temp file descriptor
os.close(temp_fd)

# Replace original file with deduplicated version
os.replace(temp_path, file_path)
