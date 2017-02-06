import prettytable
import __builtin__
from colorama import Fore, init, Style
from collections import OrderedDict

def display_results_ordered(results, colmn="all"):
    if colmn == 'all' and not __builtin__.short:
        columns = ['index', 'pillar', 'name', 'id', 'priv_ip', 'pub_ip', 'vpc_id', 'subnet_id', 'size', 'location',
                   'status', 'monitored', 'sc_pillar', 'sc_app', 'sc_version']
    if colmn == 'short' or __builtin__.short:
        columns = ['index', 'name', 'priv_ip', 'status']
    index = 1
    t = prettytable.PrettyTable([c.capitalize() for c in columns])
    t.align = 'l'
    for r in results:
        if r['status'] == 'stopped' and not __builtin__.running:
            r['status'] = Fore.RED + 'stopped' + Style.RESET_ALL
            t.add_row([index] + [r[x] for x in columns[1:]])
            index += 1
        elif r['status'] == 'running' and not __builtin__.stopped:
            t.add_row([index] + [r[x] for x in columns[1:]])
            index += 1

    print(t)
