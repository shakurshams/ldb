import pandas as pd


def parse(path):
    uni_data = pd.read_csv(
        path,
        header=0,
        delimiter="\t"
    )

    return uni_data
