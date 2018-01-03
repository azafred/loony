import prettytable
import config
from colorama import Fore, Style

def format_cell(content, max_line_length):
    #accumulated line length
    ACC_length = 0
    words = content.split(" ")
    formatted_content = ""
    for word in words:
        #if ACC_length + len(word) and a space is <= max_line_length 
        if ACC_length + (len(word) + 1) <= max_line_length:
            #append the word and a space
            formatted_content = formatted_content + word + " "
            #length = length + length of word + length of space
            ACC_length = ACC_length + len(word) + 1
        else:
            #append a line break, then the word and a space
            formatted_content = formatted_content + "\n" + word + " "
            #reset counter of length to the length of a word and a space
            ACC_length = len(word) + 1
    return formatted_content


def display_results_ordered(results, notable='', cell_length=100):
    if config.short:
        display_columns = ['index', 'name', 'priv_ip', 'status', 'tags_txt']
    elif config.long_format:
        display_columns = ['index', 'name', 'id', 'priv_ip', 'pub_ip', 'vpc_id', 'subnet_id', 'size', 'location',
                        'status', 'monitored', 'launch_time', 'env', 'role', 'master', 'cfn_stack_name', 'as_group_name']
    elif config.devstack_format:
        display_columns = ['index', 'name', 'priv_ip', 'bigdata', 'branch', 'es_status', 'rev', 'launch_time']
    elif not config.output or config.output == 'normal':
        display_columns = ['index', 'name', 'id', 'priv_ip', 'size', 'launch_time', 'tags_txt']
    else:
        display_columns = config.output


    t = prettytable.PrettyTable([c.capitalize() for c in display_columns])
    t.align = 'l'
    # sorted_results = sorted(results, key=itemgetter('env', 'role', 'launch_time'))

    for r in results:
        # tags = str(r['tags'])
        for x in display_columns:
            if isinstance(r[x], basestring):
                if r[x].lower() in ['red', 'false']:
                    r[x] = Fore.RED + r[x] + Style.RESET_ALL
                elif r[x].lower() in ['green', 'true']:
                    r[x] = Fore.GREEN + r[x] + Style.RESET_ALL
                elif r[x].lower() in ['yellow']:
                    r[x] = Fore.YELLOW + r[x] + Style.RESET_ALL
        if 'true' in r.get('master', ''):
            # t.add_row([Fore.RED + format_cell(str(r[x]), cell_length) + Style.RESET_ALL for x in display_columns])
            t.add_row([Fore.RED + format_cell(str(r.get(x, 'N/A')), cell_length) + Style.RESET_ALL for x in display_columns])
        else:
            t.add_row([format_cell(str(r.get(x, "N/A")), cell_length) for x in display_columns])
            # t.add_row([format_cell(str(r[x]), cell_length) for x in display_columns])
    if notable:
        print(t.get_string(border=False, padding_width=1, header=False))
    else:
        print(t)
