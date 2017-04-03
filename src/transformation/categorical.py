import pandas as pd


def tranform(dataframe, omit):
    categorical_headers = list(dataframe.select_dtypes(
        include=['category', 'object']).columns)

    _remove_if_contains(categorical_headers, omit)

    result = dataframe.copy()

    for x in categorical_headers:
        dummies = _transform(x, result)
        # there is no inplace concat, in the end numpy concatenate will get
        # called and new array will be allocated
        result = pd.concat([result, dummies], axis=1)
        result.__delitem__(x)

    new_headers = list(result.columns)
    _remove_if_contains(new_headers, omit)
    return result, new_headers


def _remove_if_contains(from_list, remove):
    for o in remove:
        if o in from_list:
            from_list.remove(o)


def _transform(column, result):
    dummies = pd.get_dummies(result[column])
    dummies.rename(columns=lambda x: "%s/%s" % (column, x), inplace=True)
    return dummies
