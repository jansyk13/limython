def _parse_kwargs(kwargs):
    if (not kwargs):
        return {}
    result = {}
    key_values = kwargs.split(",")
    for key_value in key_values:
        split = key_value.split("=")
        result[split[0]] = try_parse(split[1])
    return result


def try_parse(value):
    if (value == u'true'):
        return True
    if (value == u'false'):
        return False
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value
