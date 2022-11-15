import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-e", "--expressions", action="append")
def rex(argv, results):
    args = parser.parse_args(argv)
    expressions = [re.compile(ex) for ex in args.expressions]
    for event in results:
        for expression in expressions:
            if match := expression.search(event["text"]):
                event["extracted_fields"].update(match.groupdict())
        yield event
        
