import csv
import os
import re

import unicodedata


def filter_csv(input_file, field1, field2):
    with open(input_file, 'r') as f:
        reader = csv.DictReader(f)
        filtered_data = []
        for row in reader:
            source = re.sub(r'[^\w\s]|[\xa0]', ' ', re.sub(r'[À-ÖØ-öø-ÿ]', '', row['sourceName']))
            if source == field1 and row['type'] == field2:
                filtered_data.append(row)
    output_file = os.path.join("output/splitted", f"{field1}_{field2}.csv")
    with open(output_file, 'w', newline='') as f:
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in filtered_data:
            writer.writerow(row)
    return output_file

