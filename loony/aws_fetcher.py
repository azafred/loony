import boto.ec2
from datetime import datetime, timedelta
import animation
from cache import scached
from settings import *
from operator import itemgetter
#from decorating import animated

## TODO: Fix this sillyness and merge dicts instead of having to manually add each tag.

@scached(cache_file=cache_file, expiry=timedelta(minutes=cache_lifetime))
#@animated('Loading data')
@animation.wait('Loading data')
def aws_inventory():
    instances = []
    index = 1
    conn = boto.connect_ec2()
    reservations = conn.get_all_instances()
    for res in reservations:
        for inst in res.instances:
            id = inst.id
            name = inst.tags.get('Name', 'NoName')
            location = inst.placement
            launch_time = str(inst.launch_time)
            size = inst.instance_type
            public_ip = inst.ip_address or ''
            private_ip = inst.private_ip_address or ''
            pub_dns = inst.public_dns_name or ''
            priv_dns = inst.private_dns_name or ''
            vpc_id = inst.vpc_id or ''
            subnet_id = inst.subnet_id or ''
            env = inst.tags.get('Env', '')
            role = inst.tags.get('Role', '')
            master = inst.tags.get('master', '')
            es_cluster = inst.tags.get('es_cluster', '')
            bigdata = inst.tags.get('bigdata', '')
            es_status = inst.tags.get('es_status', '')
            rev = inst.tags.get('rev', '')
            branch = inst.tags.get('branch', '')
            cfn_logical_id = inst.tags.get('aws:cloudformation:logical-id', '')
            cfn_stack_id = inst.tags.get('aws:cloudformation:stack-id', '')
            cfn_stack_name = inst.tags.get('aws:cloudformation:stack-name', '')
            as_group_name = inst.tags.get('aws:autoscaling:groupName', '')
            active_link = inst.tags.get('active_link', '')
            num_links_connected = inst.tags.get('num_link_connected', '')
            # Stringing tags that are not relevant to indexing
            other_tags = {}
            for (key, val) in inst.tags.items():
                if 'aws' not in key and 'Name' not in key and 'Hostname' not in key:
                    other_tags[key] = str(val)
            tags_txt = ', '.join("{!s}={!r}".format(key, val) for (key, val) in sorted(other_tags.items()))
            monitored = inst.monitored
            if inst.state in 'running':
                instances.append({'id': id, 'name': name, 'location': location,
                                    'size': size,
                                    'pub_ip': public_ip, 'priv_ip': private_ip, 'pub_dns': pub_dns,
                                    'priv_dns': priv_dns,
                                    'status': inst.state, 'vpc_id': vpc_id, 'subnet_id': subnet_id,
                                    'monitored': monitored, 'tags': dict(inst.tags), 'tags_txt': tags_txt,
                                    'env': env, 'role': role, 'master': master,
                                    'cfn_logical_id': cfn_logical_id, 'cfn_stack_id': cfn_stack_id,
                                    'cfn_stack_name': cfn_stack_name,
                                    'as_group_name': as_group_name,
                                    'launch_time': launch_time,
                                    'es_cluster': es_cluster,
                                    'es_status': es_status,
                                    'bigdata': bigdata,
                                    'branch': branch,
                                    'rev': rev,
                                    'active_link': active_link,
                                    'num_links_connected': num_links_connected})
    sorted_instances = sorted(instances, key=itemgetter('env', 'role', 'launch_time'))
    for s in sorted_instances:
        s['index'] = index
        index += 1
    return sorted_instances

def list_keys():
    instances = aws_inventory()
    keys = sorted(instances[0].keys())
    print "The following keys are available:"
    print ", ".join(keys)
