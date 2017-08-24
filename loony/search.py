import __builtin__
import re
from aws_fetcher import aws_inventory
from display import display_results_ordered
from pprint import pprint
from operator import itemgetter



def recurse_search(search, item, original_item=''):
    pattern = re.compile(search)
    if not original_item:
        original_item = search
    if isinstance(item, dict):
        for k,v in item.iteritems():
            recurse_search(search, v, original_item)
    elif isinstance(item, list):
        for i in item:
            recurse_search(search, i, original_item)
    elif isinstance(item, str) or isinstance(item, unicode):
            #if search in item:
            if re.search(pattern, item):
                return True
    return False


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
                pattern = re.compile(value)
                # This is a filtered search
                # if inst[key].lower() == value:
                key = key.lower()
                if re.search(pattern, inst[key]):
                # if value in inst[key.lower()]:
                    if filter(lambda id: id['id'] == inst['id'], results_per_item[item]):
                        pass
                    else:
                        results_per_item[item].append(inst)
                        try:
                            result_counter[inst['id']] += 1
                        except:
                            result_counter[inst['id']] = 1
            else:
                # This is an everything search
                for k, v in inst.iteritems():
                    #if item in str(v).lower():
                    if recurse_search(item, v):
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

    if len(result) >= 1:
        # print and_result

        sorted_results = sorted(result, key=itemgetter('env', 'role', 'launch_time'))
        for s in sorted_results:
            s['index'] = index
            index += 1
        display_results_ordered(sorted_results, notable=notable)
    return result
