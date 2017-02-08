import ConfigParser
import os


def read_aws_domains(ignored_domains):
    cred_file = os.path.expanduser('~/.aws/credentials')
    try:
        creds = ConfigParser.ConfigParser()
        creds.readfp(open(cred_file))
    except:
        print "There is a problem with your aws credentials. Please read the README for Loony."
    aws_domains = creds.sections()
    result = []
    for aws_domain in aws_domains:
        if 'default' not in aws_domain and aws_domain not in ignored_domains:
            result.append(aws_domain)
    return result
