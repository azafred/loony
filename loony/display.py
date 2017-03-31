import prettytable
import __builtin__
from colorama import Fore, Style

def display_results_ordered(results):
    if __builtin__.short:
        display_columns = ['index', 'name', 'priv_ip', 'status', 'tags_txt']
    elif __builtin__.long:
        display_columns = ['index', 'name', 'id', 'priv_ip', 'pub_ip', 'vpc_id', 'subnet_id', 'size', 'location',
                   'status', 'monitored', 'launch_time', 'Env', 'Role', 'Master', 'cfn_stack_name']
    elif not __builtin__.output or __builtin__.output == 'normal':
        display_columns = ['index', 'name', 'id', 'priv_ip', 'size', 'launch_time', 'tags_txt']
    else:
        display_columns = __builtin__.output


    t = prettytable.PrettyTable([c.capitalize() for c in display_columns])
    t.align = 'l'
    for r in results:
        # tags = str(r['tags'])
        if r['status'] == 'stopped' and not __builtin__.running:
            r['status'] = Fore.RED + 'stopped' + Style.RESET_ALL
            t.add_row([r[x] for x in display_columns])
        elif r['status'] == 'running' and not __builtin__.stopped:
            t.add_row([r[x] for x in display_columns])
    print(t)
