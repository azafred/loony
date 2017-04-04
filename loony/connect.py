from subprocess import call
from display import display_results_ordered
from settings import *
import sys
import libtmux


def connect_to(instances, user='', cmd='', batch=''):
    ssh_opt = " -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no "
    if user:
        cmd_usr = ' -l %s ' % user
    else:
        cmd_usr = ' '
    print "choices of %s instances" % len(instances)
    if len(instances) < 2 or batch:
        print("Note: make sure you are connected to the VPN!")
        for inst in instances:
            ip = inst['priv_ip']
            name = inst['name']
            print("connecting to: %s - %s " % (name, ip))
            if cmd:
                call("ssh" + ssh_opt + cmd_usr + ip + " " + cmd, shell=True)
            else:
                call("ssh" + ssh_opt + cmd_usr + ip, shell=True)
        sys.exit(0)
    elif len(instances) <= 18:
        # use tmux!
        init_tmux(instances, user=user, cmd=cmd)
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
                if cmd:
                    print("Running %s on %s" % (cmd, inst['name']))
                    call("ssh" + ssh_opt + cmd_usr + ip + " " + cmd, shell=True)
                else:
                    call("ssh" + ssh_opt + cmd_usr + ip, shell=True)
                sys.exit(0)


def init_tmux(instances, title='loony', cmd='', user=''):
    logmap = [{'role': 'webapp', 'log': '/var/log/tomcat-webapp/studyblue.log'},
              {'role': 'openapi', 'log': '/var/log/tomcat-openapi/openapi.log'}]
    ssh_opt = " -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no "
    num_panes = 6
    pindex = 0
    windex = 0
    new_window = True
    if user:
        cmd_usr = ' -l %s ' % user
    else:
        cmd_usr =' '
    server = libtmux.Server()
    session = server.new_session(title)
    # some logic and if loops here....
    w = session.select_window('@0')
    for inst in instances:
        if pindex % num_panes == 0 and pindex != 0:
            blah = title + str(pindex)
            w = session.new_window(attach=False, window_name=blah)
            windex += 1
            new_window = True
            x = '@%s' % windex
            w = session.select_window(x)
        p = w.split_window(attach=True, vertical=True)
        if new_window:
            if windex == 0:
                index = '%%%i' % (pindex * windex)
            else:
                index = '%%%i' % (pindex * windex + windex)
            b = w.select_pane(index)
            b.cmd('kill-pane')
            new_window=False
        p.send_keys("echo 'connecting to  %s'" % inst['name'])
        # p.send_keys("echo %s | figlet" % inst['name'])
        p.send_keys("ssh" + ssh_opt + cmd_usr + inst['priv_ip'])
        if cmd == 'logs':
            pass
        elif cmd:
            p.send_keys(cmd)
        pindex += 1
        w.select_layout('tiled')
    w.select_layout('tiled')
    session.attach_session()
