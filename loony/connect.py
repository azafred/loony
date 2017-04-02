from subprocess import call
from display import display_results_ordered
from settings import *
import sys
import libtmux


def connect_to(instances, user=''):
    if user:
        cmd_usr = ' -l %s ' % user
    print "choices of %s instances" % len(instances)
    if len(instances) < 2:
        print("Note: make sure you are connected to the VPN!")
        ip = instances[0]['priv_ip']
        print("Connecting to %s" % ip)
        call("ssh" + cmd_usr + ip, shell=True)
        sys.exit(0)
    elif len(instances) <= 18:
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
                call("ssh" + cmd_usr + ip, shell=True)
                sys.exit(0)
    print("An error has occured.")


def init_tmux(instances, title='loony', cmd='', user=''):
    pindex = 0
    if user:
        cmd_usr = ' -l %s ' % user
    server = libtmux.Server()
    session = server.new_session(title)
    num_of_panes = len(instances)
    # some logic and if loops here....
    w = session.new_window(attach=False, window_name=title)
    for inst in instances:
        if pindex % 6 == 0 and pindex != 0:
            w = session.new_window(attach=False, window_name=title)
        if pindex % 2 == 0:
            p[inst] = w.split_window(attach=False)
        else:
            p[inst] = w.split_window(attache=False, vertical=False)
        p[inst].send_keys("ssh" + cmd_usr + inst['priv_ip'])
        pindex += 1
    # p2 = w.split_window(attach=False, window_name="blah", vertical=False)
    session.attach_session()
