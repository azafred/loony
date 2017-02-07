import __builtin__
from aws_fetcher import aws_inventory
from display import display_results_ordered

## TODO: nested items search...

def searchfor(items):
    if __builtin__.verbose:
        print 'verbose'
    aws = aws_inventory()
    result = []
    index = 1
    for inst in aws:
        #print inst.values()
        for item in items:
            if item in inst.values() or item in inst['name']:
                if inst not in result:
                    inst['index'] = index
                    index += 1
                    result.append(inst)
    if len(result) >= 1:
        display_results_ordered(result)
    return result

def pub_ip():
    aws = aws_inventory()
    result = []
    for inst in aws:
        if inst['pub_ip']:
            if inst not in result:
                result.append(inst)
    if len(result) >= 1:
        display_results_ordered(result)
    return result