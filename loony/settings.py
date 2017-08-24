import os

user = os.environ['USER']
cache_file = '/tmp/' + user + '-loonycache'
prefered_output = "normal" # could be short, all or a list of columnts
cache_lifetime = 1440 #in minutes
display_tags = ['Env', 'Role', 'master']
index_tags = ['aws:cloudformation:logical-id', 'aws:cloudformation:stack-id', 'aws:cloudformation:stack-name', 'aws:autoscaling:groupName']

