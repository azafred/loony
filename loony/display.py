import prettytable
import __builtin__
from colorama import Fore, Style

def test(blah=''):
    blah = __builtin__.output
    print blah

def display_results_ordered(results):

    if __builtin__.short:
        display_columns = ['index', 'name', 'priv_ip', 'status']
    elif __builtin__.long:
        display_columns = ['index', 'pillar', 'name', 'id', 'priv_ip', 'pub_ip', 'vpc_id', 'subnet_id', 'size', 'location',
                   'status', 'monitored', 'sc_pillar', 'sc_app', 'sc_version', 'launch_time']
    elif not __builtin__.output or __builtin__.output == 'normal':
        display_columns = ['index', 'name', 'id', 'priv_ip', 'size', 'sc_app', 'sc_version']
    else:
        display_columns = __builtin__.output


    t = prettytable.PrettyTable([c.capitalize() for c in display_columns])
    t.align = 'l'
    for r in results:
        if r['status'] == 'stopped' and not __builtin__.running:
            r['status'] = Fore.RED + 'stopped' + Style.RESET_ALL
            t.add_row([r[x] for x in display_columns])
        elif r['status'] == 'running' and not __builtin__.stopped:
            t.add_row([r[x] for x in display_columns])
    print(t)
