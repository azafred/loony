from config_parser import read_aws_domains

cache_file = '/tmp/aws_inventory'
# default_aws_domains = ['ops', 'qa', 'prod', 'experiments']
ignored_aws_domains=['fred']
default_aws_domains = read_aws_domains(ignored_aws_domains)
prefered_output = "all"
ssh_as = 'ubuntu'
cache_lifetime = 60 #in minutes


