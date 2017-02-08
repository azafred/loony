import prettytable
import __builtin__
from colorama import Fore, Style

def test(blah=''):
    blah = __builtin__.output
    print blah

def display_results_ordered(results, colmn="all"):
    if 'all' not in __builtin__.output:
        columns = __builtin__.output
    elif colmn == 'all' and not __builtin__.short:
        columns = ['index', 'pillar', 'name', 'id', 'priv_ip', 'pub_ip', 'vpc_id', 'subnet_id', 'size', 'location',
                   'status', 'monitored', 'sc_pillar', 'sc_app', 'sc_version']
    elif colmn == 'short' or __builtin__.short:
        columns = ['index', 'name', 'priv_ip', 'status']
    elif colmn == 'normal':
        columns = ['index', 'name', 'id', 'priv_ip', 'size', 'sc_app', 'sc_version']
    t = prettytable.PrettyTable([c.capitalize() for c in columns])
    t.align = 'l'
    for r in results:
        if r['status'] == 'stopped' and not __builtin__.running:
            r['status'] = Fore.RED + 'stopped' + Style.RESET_ALL
            t.add_row([r[x] for x in columns])
        elif r['status'] == 'running' and not __builtin__.stopped:
            t.add_row([r[x] for x in columns])
    print(t)
