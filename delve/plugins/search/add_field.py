import argparse

parser = argparse.ArgumentParser()
parser.add_argument("fieldname", type=str, help="The name of the field to add to extracted_fields")
def add_field(argv, results):
    args = parser.parse_args(argv)
    fieldname = args.fieldname
    for result in results:
        result["extracted_fields"][fieldname] = result[fieldname]
        yield result
