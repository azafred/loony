import __builtin__
from aws_fetcher import aws_inventory
from display import display_results_ordered

def searchfor(items, oroperand=False):
    if __builtin__.verbose:
        print 'verbose'
    aws = aws_inventory()
    or_result = []
    result_per_item = {}
    and_result = []
    counter = {}
    index = 1
    for item in items:
        result_per_item[item] = []
    for inst in aws:
        for item in items:
            if inst['status'] == 'stopped' and __builtin__.running:
                break
            if inst['status'] == 'running' and __builtin__.stopped:
                break
            if item in inst['name']:
                try:
                    counter[inst['id']] += 1
                except:
                    counter[inst['id']] = 1
                if inst not in or_result:
                    or_result.append(inst)
                result_per_item[item].append(inst)
            for k,v in inst.items():
                if item in str(v):
                    try:
                        counter[inst['id']] += 1
                    except KeyError:
                        counter[inst['id']] = 1
                    if inst not in or_result:
                        or_result.append(inst)
                    result_per_item[item].append(inst)
    if not oroperand:
        for k,v in counter.iteritems():
            if v == len(items):
                for inst in aws:
                    if inst['id'] == k:
                        and_result.append(inst)
        for r in and_result:
            r['index'] = index
            index += 1
        if len(and_result) >= 1:
            display_results_ordered(and_result)
        return and_result
    else:
        for r in or_result:
            r['index'] = index
            index += 1
        if len(or_result) >= 1:
            display_results_ordered(or_result)
        return or_result

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