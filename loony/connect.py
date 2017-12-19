from __future__ import print_function
from subprocess import call, Popen
from loony.display import display_results_ordered
from loony.settings import *
from colorama import Fore, Style
import sys
import os
import libtmux
import shlex
import random
import subprocess

FNULL = open(os.devnull, 'w')


def is_tmux():
    signal = call(['which', 'tmux'], stderr=subprocess.STDOUT)
    if signal == 0:
        return True
    else:
        print("Tmux not detected. I recommend you install it! (on mac: brew install tmux)")
        return False


def is_iterm():
    try:
        term = os.environ['TERM_PROGRAM']
        if term == 'iTerm.app':
            return True
        else:
            print("It doesn't appear that you are running iTerm. If you are on a mac, I would strongly recommend it for its useful tmux integration!")
            return False
    except:
        return False


def connect_to(instances, user='', cmd='', batch='', one_only='', public=False):
    ssh_opt = " -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no "
    if user:
        cmd_usr = ' -l %s ' % user
    else:
        cmd_usr = ' '
    print("choices of %s instances" % len(instances))
    if len(instances) < 2 or batch and not one_only:
        if len(instances) < 2 and cmd == "logs":
            if public:
                ip = instances[0]['pub_ip']
            else:
                ip = instances[0]['priv_ip']
            name = instances[0]['name']
            print("connecting to: %s - %s " % (name, ip))
            init_tmux(instances, title='logs', cmd='logs', user=user)
        else:
            print("Note: make sure you are connected to the VPN!")
            for inst in instances:
                if public:
                    ip = inst['pub_ip']
                else:
                    ip = inst['priv_ip']
                name = inst['name']
                if cmd:
                    # print("[{}]".format(name))
                    # sys.stdout.flush()
                    proc = Popen("ssh" + ssh_opt + cmd_usr + ip + " " + cmd, shell=True, stderr=FNULL, stdout=subprocess.PIPE)
                    output = proc.stdout.read()
                    for lines in output.splitlines():
                        print(Fore.BLUE + "[{: >40}]\t".format(name) + Style.RESET_ALL, end='')
                        print("{}".format(lines))
                else:
                    print("connecting to: %s - %s " % (name, ip))
                    call("ssh" + ssh_opt + cmd_usr + ip, shell=True)
            sys.exit(0)
    # elif len(instances) <= 18 and not one_only and is_tmux():
    #     # use tmux!
    #     init_tmux(instances, user=user, cmd=cmd)
    #     pass
    else:
        dest = raw_input("Connect to instance(s) number: (0 to quit, 'a' for all) ")
        dest = dest.split()
        # print("dest: %s" % dest)
        if dest[0] == '0':
            print("Bailing out!")
            sys.exit(0)
        if dest[0] == 'a':
            print("Connecting to all the instances listed above!")
            init_tmux(instances, user=user, cmd=cmd, public=public)
        if len(dest) == 1:
            print("Connecting to a single instance:")
            for inst in instances:
                if int(inst['index']) == int(dest[0]):
                    if public:
                        ip = inst['pub_ip']
                    else:
                        ip = inst['priv_ip']
                    print("Note: make sure you are connected to the VPN!")
                    print("connecting to: %s " % ip)
                    if cmd:
                        print("Running %s on %s" % (cmd, inst['name']))
                        call("ssh" + ssh_opt + cmd_usr + ip + " " + cmd, shell=True)
                    else:
                        call("ssh" + ssh_opt + cmd_usr + ip, shell=True)
                    sys.exit(0)
        else:
            targets = []
            print("Connecting to multiple targets:")
            for inst in instances:
                for i in dest:
                    if inst['index'] == int(i):
                        targets.append(inst)
            if len(targets) > 1:
                init_tmux(targets, user=user, cmd=cmd, public=public)
            else:
                print("No target found.")


def init_tmux(instances, title='loony', cmd='', user='', public=False):
    systemlogs = ['/var/log/messages', '/var/log/secure', '/var/log/tallylog']
    logmap = [{'role': 'webapp', 'log': ['/var/log/tomcat-webapp/*.log', '/var/log/tomcat-webapp/catalina.out']},
              {'role': 'openapi', 'log': ['/var/log/tomcat-openapi/*.log', '/var/log/tomcat-openapi/catalina.out']},
              {'role': 'web', 'log': ['/var/log/tomcat*/*']}]
    ssh_opt = " -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no "
    num_panes = 6
    pindex = 0
    windex = 0
    new_window = True
    if user:
        cmd_usr = ' -l %s ' % user
    else:
        cmd_usr = ' '
    server = libtmux.Server()
    rand_session = random.randint(1, 100)
    rand_title = title + str(rand_session)
    session = server.new_session(rand_title, kill_session=True)
    # some logic and if loops here....
    w = session.windows[0]
    for inst in instances:
        if pindex % num_panes == 0 and pindex != 0:
            blah = title + str(pindex)
            w = session.new_window(attach=False, window_name=blah)
            windex += 1
            new_window = True
            # x = '@%s' % windex
            w = session.windows[windex]
            # w = session.select_window(x)
        p = w.split_window(attach=True, vertical=True)
        if new_window:
            b = w.panes[0]
            b.cmd('kill-pane')
            new_window = False
        p.send_keys("echo 'connecting to  %s'" % inst['name'])
        # p.send_keys("echo %s | figlet" % inst['name'])
        if public:
            p.send_keys("ssh" + ssh_opt + cmd_usr + inst['pub_ip'])
        else:
            p.send_keys("ssh" + ssh_opt + cmd_usr + inst['priv_ip'])
        if cmd == 'logs':
            role = inst['role']
            try:
                logfile = (item['log'] for item in logmap if item['role'] == role).next()
                logs = " ".join(logfile)
            except:
                logs = " ".join(systemlogs)
            p.send_keys("echo 'tailing the following logs: %s'" % logs)
            p.send_keys("sudo tail -n 0 -fq  %s | grep -v 'network_id cookie not set'" % logs)
        elif cmd == 'syslogs':
            logs = " ".join(systemlogs)
            p.send_keys("echo 'tailing the following logs: %s'" % logs)
            p.send_keys("sudo tail -n 0 -fq  %s " % logs)
        elif cmd:
            p.send_keys(cmd)
        pindex += 1
        w.select_layout('tiled')
    w.select_layout('tiled')
    # session.attach_session()
    if is_iterm():
        tmux = shlex.split("tmux -CC attach")
        call(tmux)
    else:
        session.attach_session()

