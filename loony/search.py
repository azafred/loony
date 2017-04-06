import __builtin__
from aws_fetcher import aws_inventory
from display import display_results_ordered
from pprint import pprint

def searchfor(items, notable=''):
    aws = aws_inventory()
    results_per_item = {}
    result_counter = {}
    result = []
    index = 1
    for item in items:
        results_per_item[item] = []
    for inst in aws:
        for item in items:
            if '=' in item:
                key, value = item.split('=')
                # This is a filtered search
                if inst[key] == value:
                    if filter(lambda id: id['id'] == inst['id'], results_per_item[item]):
                        pass
                    else:
                        results_per_item[item].append(inst)
                        try:
                            result_counter[inst['id']] += 1
                        except:
                            result_counter[inst['id']] = 1
                            
            else:
                # This is a everything search
                for k, v in inst.items():
                    if item in str(v):
                        # Only add instance if it is not already in the list...
                        if filter(lambda id: id['id'] == inst['id'], results_per_item[item]):
                            pass
                        else:
                            results_per_item[item].append(inst)
                            try:
                                result_counter[inst['id']] += 1
                            except:
                                result_counter[inst['id']] = 1

    for k, v in result_counter.iteritems():
        if v == len(items):
            for inst in aws:
                if inst['id'] == k and 'running' in inst['status']:
                    result.append(inst)
    for r in result:
        r['index'] = index
        index += 1
    if len(result) >= 1:
        # print and_result
        display_results_ordered(result, notable=notable)
    return result
