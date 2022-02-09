def find_dict_keys(srch_dict: dict, fields: list) -> list:
    fields_found = []
    for key, value in srch_dict.items():
        if key in fields:
            fields_found.append(key)

        if isinstance(value, dict):
            results = find_dict_keys(value, fields)
            for result in results:
                fields_found.append(result)

        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    more_results = find_dict_keys(item, fields)
                    for another_result in more_results:
                        fields_found.append(another_result)
    return fields_found


def validate_dict_keys(srch_dict: dict, valid_keys: list) -> None:
    found_keys = set(
        find_dict_keys(srch_dict, valid_keys)
    )
    invalid_keys = set(valid_keys).difference(found_keys)
    if len(found_keys) != len(valid_keys):
        msg = "\n*Cause: The following keys were not found: [{}]".format(
            ", ".join(
                f"'{key}'" for key in sorted(invalid_keys)
            )
        ) + "\n*Action: The dictionary must contain all the following keys:" \
            " [{}]".format(
                ", ".join(
                    f"'{key}'" for key in sorted(set(valid_keys))
                )
            )
        raise ValueError(msg)


def instance_of(value, attr_type) -> None:
    if not isinstance(value, attr_type):
        actual = value.__class__
        msg = (
            f"\n*Cause: The object must be type of '{attr_type}' "
            f"and got an object of type '{actual}'"
            "\n*Action: Set the the appropiate data type "
            f"for the passed value({value})"
        )
        raise TypeError(msg)
