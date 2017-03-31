from subprocess import call
from display import display_results_ordered
from settings import *
import sys
import libtmux


def connect_to(instances, user='ec2-user'):
    print "choices of %s instances" % len(instances)
    if len(instances) < 2:
        print("Note: make sure you are connected to the VPN!")
        ip = instances[0]['priv_ip']
        print("Connecting to %s" % ip)
        call("ssh -l " + user + " " + ip, shell=True)
        sys.exit(0)
    elif len(instances) <= 10:
        # use tmux!
        init_tmux(instances, user=user)
        pass
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
                call("ssh -l " + user + " " + ip, shell=True)
                sys.exit(0)
    print("An error has occured.")


def init_tmux(instances, title='loony', cmd='', user='ec2_user'):
    server = libtmux.Server()
    session = server.new_session(title)
    num_of_panes = len(instances)
    # some logic and if loops here....
    w = session.new_window(attach=False, window_name="blah")
    for inst in instances:
        p1 = w.split_window(attach=False, window_name=inst['Name'])
        p1.send_keys("ssh -l " + user + " " + inst['ip'])
    # p2 = w.split_window(attach=False, window_name="blah", vertical=False)
    session.attach_session()
