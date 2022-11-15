import argparse

import pandas as pd

parser  = argparse.ArgumentParser()
parser.add_argument("--extracted", action="store_true", help="only include extracted_fields")
def to_df(argv, results):
    args  = parser.parse_args(argv)
    if args.extracted:
        df = pd.DataFrame([result["extracted_fields"] for result in results])
    else:
        df = pd.DataFrame(results)
    return df
