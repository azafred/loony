import boto.ec2
import datetime
import __builtin__
from cache import scached
from settings import *

@scached(cache_file=cache_file, expiry=datetime.timedelta(minutes=cache_lifetime))
def aws_inventory(create_index=False):
    instance = []
    index = 1
    profiles = default_aws_domains
    for p in profiles:
        conn=boto.connect_ec2(profile_name=p)
        reservations = conn.get_all_instances()
        for res in reservations:
            for inst in res.instances:
                id = inst.id
                try:
                    name = inst.tags['Name']
                except:
                    name = 'NoName'
                location = inst.placement
                launch_time = inst.launch_time
                size = inst.instance_type
                try:
                    public_ip = inst.ip_address
                except:
                    public_ip = 'No Pub_IP'
                private_ip = inst.private_ip_address
                try:
                    pub_dns = inst.public_dns_name
                except:
                    pub_dns = 'No public DNS'
                try:
                    priv_dns = inst.private_dns_name
                except:
                    priv_dns = 'No private DNS'
                try:
                    vpc_id = inst.vpc_id
                except:
                    vpc_id = 'No VPC'
                try:
                    subnet_id = inst.subnet_id
                except:
                    subnet_id = 'No Subnet'
                try:
                    sc_app = inst.tags['sc_app']
                except:
                    sc_app = ''
                try:
                    sc_pillar = inst.tags['sc_pillar']
                except:
                    sc_pillar = ''
                try:
                    sc_version = inst.tags['sc_version']
                except:
                    sc_version = ''
                monitored = inst.monitored
                if create_index:
                    instance.append({'index': index, 'pillar': p, 'id': id, 'name': name, 'location': location, 'size': size,
                                     'pub_ip': public_ip, 'priv_ip': private_ip, 'pub_dns': pub_dns,
                                     'priv_dns': priv_dns,
                                     'status': inst.state, 'vpc_id': vpc_id, 'subnet_id': subnet_id,
                                     'monitored': monitored,
                                     'sc_app': sc_app, 'sc_pillar': sc_pillar, 'sc_version': sc_version, 'launch_time': launch_time})
                    index += 1
                else:
                    instance.append({'pillar': p, 'id': id, 'name': name, 'location': location, 'size': size,
                                     'pub_ip': public_ip, 'priv_ip': private_ip, 'pub_dns': pub_dns, 'priv_dns': priv_dns,
                                     'status': inst.state, 'vpc_id': vpc_id, 'subnet_id': subnet_id, 'monitored': monitored,
                                     'sc_app': sc_app, 'sc_pillar': sc_pillar, 'sc_version':sc_version, 'launch_time': launch_time})
    return instance
