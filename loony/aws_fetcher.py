import boto.ec2
import datetime
from cache import scached


@scached(cache_file='/tmp/aws_inventory', expiry=datetime.timedelta(minutes=50))
def aws_inventory():
    instance = []
    profiles = ['ops', 'qa', 'prod', 'experiments']
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
                monitored = inst.monitored

                instance.append({'pillar': p, 'id': id, 'name': name, 'location': location, 'size': size,
                                 'pub_ip': public_ip, 'priv_ip': private_ip, 'pub_dns': pub_dns, 'priv_dns': priv_dns,
                                 'status': inst.state, 'vpc_id': vpc_id, 'subnet_id': subnet_id, 'monitored': monitored})
    return instance
