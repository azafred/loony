import __builtin__
from aws_fetcher import aws_inventory
from display import display_results_ordered

def searchfor(items, oroperand=False):
    if __builtin__.verbose:
        print 'verbose'
    aws = aws_inventory()
    result = []
    result_per_item = {}
    out = []
    counter = {}
    index = 1
    for item in items:
        result_per_item[item] = []
    for inst in aws:
        for item in items:
            if item in inst.values() or item in inst['name']:
                try:
                    counter[inst['id']] += 1
                except KeyError:
                    counter[inst['id']] = 1
                if inst not in result:
                    inst['index'] = index
                    index += 1
                    result.append(inst)
                result_per_item[item].append(inst)
    if not oroperand:
        for k,v in counter.iteritems():
            if v == len(items):
                for inst in aws:
                    if inst['id'] == k:
                        out.append(inst)
        if len(out) >= 1:
            display_results_ordered(out)
        return out
    else:
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