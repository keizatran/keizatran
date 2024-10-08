import pandas as pd


def convert_to_utf8(data):

    if isinstance(data, pd.Series):
        return data.str.encode("latin1", "ignore").str.decode("utf-8", "ignore")
    elif isinstance(data, dict):
        return {key: convert_to_utf8(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_to_utf8(element) for element in data]
    elif isinstance(data, str):
        return data.encode("latin1", "ignore").decode("utf-8", "ignore")
    else:
        return data
