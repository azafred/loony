from __future__ import absolute_import
import re
from .aws_fetcher import aws_inventory
from .display import display_results_ordered
from pprint import pprint
from operator import itemgetter
import six



def recurse_search(search, item, original_item=''):
    pattern = re.compile(search)
    if not original_item:
        original_item = search
    if isinstance(item, dict):
        for k,v in six.iteritems(item):
            recurse_search(search, v, original_item)
    elif isinstance(item, list):
        for i in item:
            recurse_search(search, i, original_item)
    elif isinstance(item, str) or isinstance(item, six.text_type):
            #if search in item:
            if re.search(pattern, item):
                return True
    return False


def searchfor(items, orsearch='', notable=''):
    aws = aws_inventory()
    results_per_item = {}
    result_counter = {}
    orresult_counter = {}
    result = []
    index = 1
    for item in items:
        results_per_item[item] = []
    for item in orsearch:
        results_per_item[item] = []
    for inst in aws:
        for item in items:
            if '=' in item:
                key, value = item.split('=')
                pattern = re.compile(value)
                key = key.lower()
                if re.search(pattern, inst[key]):
                    if [id for id in results_per_item[item] if id['id'] == inst['id']]:
                        pass
                    else:
                        results_per_item[item].append(inst)
                        try:
                            result_counter[inst['id']] += 1
                        except:
                            result_counter[inst['id']] = 1
            else:
                for k, v in six.iteritems(inst):
                    if recurse_search(item, v):
                        if [id for id in results_per_item[item] if id['id'] == inst['id']]:
                            pass
                        else:
                            results_per_item[item].append(inst)
                            try:
                                result_counter[inst['id']] += 1
                            except:
                                result_counter[inst['id']] = 1

        for item in orsearch:
            if '=' in item:
                key, value = item.split('=')
                pattern = re.compile(value)
                key = key.lower()
                if re.search(pattern, inst[key]):
                    if [id for id in results_per_item[item] if id['id'] == inst['id']]:
                        pass
                    else:
                        results_per_item[item].append(inst)
                        try:
                            orresult_counter[inst['id']] += 1
                        except:
                            orresult_counter[inst['id']] = 1
            else:
                for k, v in six.iteritems(inst):
                    if recurse_search(item, v):
                        if [id for id in results_per_item[item] if id['id'] == inst['id']]:
                            pass
                        else:
                            results_per_item[item].append(inst)
                            try:
                                orresult_counter[inst['id']] += 1
                            except:
                                orresult_counter[inst['id']] = 1

    for k, v in six.iteritems(result_counter):
        if v == len(items):
            for inst in aws:
                if inst['id'] == k and 'running' in inst['status']:
                    result.append(inst)

    for k, v in six.iteritems(orresult_counter):
        if v == len(orsearch):
            for inst in aws:
                if inst['id'] == k and 'running' in inst['status']:
                        result.append(inst)

    if len(result) >= 1:
        sorted_results = sorted(result, key=itemgetter('env', 'role', 'launch_time'))
        for s in sorted_results:
            s['index'] = index
            index += 1
        display_results_ordered(sorted_results, notable=notable)
    return result
