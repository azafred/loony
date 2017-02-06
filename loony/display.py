import prettytable

def display_results_ordered(results):
    index = 1
    t = prettytable.PrettyTable(['Index', 'Pillar', 'name', 'ID', 'Priv_IP', 'Pub_IP', 'VPC', 'Subnet', 'Size', 'AZ', 'Status', 'Monitored'])
    t.align = 'l'
    for r in results:
        t.add_row([index, r['pillar'], r['name'], r['id'], r['priv_ip'], r['pub_ip'], r['vpc_id'], r['subnet_id'], r['size'], r['location'], r['status'], r['monitored']])
        index += 1

    print t
