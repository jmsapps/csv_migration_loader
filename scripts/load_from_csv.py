import argparse
import csv

NORMALIZED_PRIMARY_KEYS = {
    "id": "_id",
}

NORMALIZED_COLUMN_NAMES = {
    "captureddate": "captured_date",
    "collectiondatetime": "collection_date",
    "dateofbirth": "date_of_birth",
    "datestarted": "period_start_date",
    "dbp": "dbp_value",
    "diabeticretinography": "diabetic_retinography",
    "diabeticretinographydate": "diabetic_retinography_date",
    "diabeticretinographykeyword": "diabetic_retinography_extracted_keyword",
    "e_prime_val": "e_prime_value",
    "elibilitycriteria": "elibility_criteria",
    "keyword": "extracted_keyword",
    "lvef_val": "lvef_value",
    "medication_source": "information_source",
    "medicationname": "medication_name",
    "nlp": "nlp_code",
    "numberresult": "result_value",
    "resultdescription": "result_description",
    "sbp": "sbp_value",
    "sentence": "source_text",
    "source": "information_source",
}

INT_COLUMN_NAMES = ["_id"]

def load_from_csv(path):
    normalization_dicts = NORMALIZED_PRIMARY_KEYS | NORMALIZED_COLUMN_NAMES
    # just to account for human error e.g. accidental camelCase in NORMALIZED_COLUMN_NAMES
    normalized_keys = {k.lower(): v for k, v in normalization_dicts.items()}

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
