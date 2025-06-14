import argparse
import csv
import sys
import os

# Ensure the `scripts/` directory is on the import path
sys.path.append(os.path.dirname(__file__))

try:
    from normalization_fields import NORMALIZATION_FIELDS
except ImportError:
    NORMALIZATION_FIELDS = {}

def load_from_csv(path):
    # just to account for human error e.g. accidental camelCase in NORMALIZED_COLUMN_NAMES
    normalized_keys = {k.lower(): v for k, v in NORMALIZATION_FIELDS.items()}

    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = []
        has_id = "_id" in [normalized_keys.get(h.lower(), h.lower()) for h in reader.fieldnames]

        for i, row in enumerate(reader):
            normalized_row = {
                normalized_keys.get(k.lower(), k.lower()): v
                for k, v in row.items()
            }

            if not has_id:
                normalized_row["_id"] = i + 1

            rows.append(normalized_row)

        return rows

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", help="Path to CSV file")
    args: str = parser.parse_args()

    print(load_from_csv(args.path))
