from subprocess import call
from display import display_results_ordered
import sys


def connect_to(instances):
    dest = raw_input("Connect to instance number: (0 to quit) ")
    dest = int(dest.strip())
    print "dest: %s" % dest
    if dest == 0:
        sys.exit(0)
    for inst in instances:
        if int(inst['index']) == dest:
            ip = inst['priv_ip']
            print("Note: make sure you are connected to the VPN!")
            print("connecting to: %s " % ip)
            call("ssh -l ubuntu " + ip, shell=True)
            sys.exit(0)
    print("An error has occured.")