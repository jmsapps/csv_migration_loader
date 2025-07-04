def coerce_items_by_validator(items, validator):
    bson_type_map = {
        "int": int,
        "string": str,
        "double": float,
        "bool": lambda v: (
            v.lower() in ("true", "1", "yes")
            if isinstance(v, str)
            else bool(v) if v is not None
            else None
        ),
        # Add more bsonType mappings as needed
    }

    schema = validator.get("$jsonSchema", {})
    props = schema.get("properties", {})

    coerced = []
    for item in items:
        new_item = {}
        for key, value in item.items():
            key_schema = props.get(key)
            if key_schema:
                bson_type = key_schema.get("bsonType")
                if isinstance(bson_type, list):
                    allowed_types = set(bson_type)
                    known = set(bson_type_map.keys())
                    allowed_non_null = allowed_types - {"null"}

                    if len(allowed_non_null) != 1 or not allowed_non_null.issubset(known):
                        raise Exception(
                            f"Invalid bsonType list for `{key}`: must be one of "
                            f"{list(bson_type_map.keys())} + 'null'"
                        )

                    actual_type = allowed_non_null.pop()
                    caster = bson_type_map.get(actual_type)

                    if value in ("", None, "null"):
                        value = None
                        caster = None  # skip casting

                else:
                    caster = bson_type_map.get(bson_type)

                if caster:
                    try:
                        value = caster(value)
                    except Exception:
                        pass  # fallback to original value if coercion fails

                if value:
                    description = key_schema.get("description", "")
                    override_rules = description.split(",")
                    for rule in override_rules:
                        rule = rule.strip()

                        if rule.startswith("coerce:"):
                            coerce_hint = rule.split("coerce:")[1]
                            if coerce_hint == "upper":
                                value = value.upper() if value not in ("", None, "null") else None
                            elif coerce_hint == "lower":
                                value = value.lower() if value not in ("", None, "null") else None
                            elif coerce_hint == "str":
                                value = str(value) if value not in ("", None, "null") else None
                            elif coerce_hint == "int":
                                value = int(value) if value not in ("", None, "null") else None
                            elif coerce_hint == "bool":
                                if isinstance(value, str):
                                    if value.lower() in ["true", "1", "yes"]:
                                        value = True
                                    elif value.lower() in ["false", "0", "no"]:
                                        value = False
                                    else:
                                        value = None
                                else:
                                    value = bool(value) if value is not None else None

            new_item[key] = value
        coerced.append(new_item)

    return coerced
