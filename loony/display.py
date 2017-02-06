import prettytable
from colorama import Fore, init, Style
from collections import OrderedDict

def display_results_ordered(results, stopped=False, running=False, colmn="all"):
    if colmn == 'all':
        columns = ['index', 'pillar', 'name', 'id', 'priv_ip', 'pub_ip', 'vpc_id', 'subnet_id', 'size', 'location',
                   'status', 'monitored', 'sc_pillar', 'sc_app', 'sc_version']
    elif colmn == 'short':
        columns = ['index', 'name', 'priv_ip', 'status']
    else:
        columns = ['index'] + colmn
    index = 1
    t = prettytable.PrettyTable([c.capitalize() for c in columns])
    t.align = 'l'
    for r in results:
        if r['status'] == 'stopped' and not running:
            r['status'] = Fore.RED + 'stopped' + Style.RESET_ALL
            t.add_row([index] + [r[x] for x in columns[1:]])
            index += 1
        elif r['status'] == 'running' and not stopped:
            t.add_row([index] + [r[x] for x in columns[1:]])
            index += 1

    print(t)
