from subprocess import call
from display import display_results_ordered
from settings import *
import sys


def connect_to(instances):

    if len(instances) == 1:
        print("Note: make sure you are connected to the VPN!")
        ip = instances[0]['priv_ip']
        print("Connecting to %s" % ip)
        call("ssh -l " + ssh_as + " " + ip, shell=True)
        sys.exit(0)
    else:
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
                call("ssh -l " + ssh_as + " " + ip, shell=True)
                sys.exit(0)
    print("An error has occured.")