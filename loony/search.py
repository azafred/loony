from aws_fetcher import aws_inventory
from display import display_results_ordered

def searchfor(items):
    aws = aws_inventory()
    result = []
    for inst in aws:
        #print inst.values()
        for item in items:
            if item in inst.values():

                if inst not in result:
                    result.append(inst)
    if len(result) >= 1:
        display_results_ordered(result)
    return result