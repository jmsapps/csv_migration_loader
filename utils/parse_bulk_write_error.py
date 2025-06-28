def parse_bulk_write_error(e):
    write_errors = getattr(e, "details", {}).get("writeErrors", [])
    if not write_errors:
        print(f"Error: {e}")

        return

    for err in write_errors:
        index = err.get("index")
        doc_id = err.get("errInfo", {}).get("failingDocumentId")
        errmsg = err.get("errmsg")
        missing_props = (
            err.get("errInfo", {})
               .get("details", {})
               .get("schemaRulesNotSatisfied", [])
        )

        # Build simplified output
        print(f"\nError at index {index}, document ID {doc_id}: {errmsg}")

        for rule in missing_props:
            operator = rule.get("operatorName")
            if operator == "required":
                missing = rule.get("propertiesNotSatisfied", [])
                print(f"  Missing required properties: {missing}")
            elif operator == "additionalProperties":
                extras = rule.get("additionalProperties", [])
                print(f"  Unexpected additional properties: {extras}")

        # Optionally print the document itself for debugging:
        print(f"Offending document: {err.get('op')}")
