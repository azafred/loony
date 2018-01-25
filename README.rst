=====
Loony
=====

This script allows for querying AWS to find the right resources when you need them.

EXAMPLES:
=========
In its simplest form, loony will simply return all the hosts running in AWS:
::

    #> loony
    Please wait while I rebuild the cache...
    +-------+------------------------------------------------------+---------------------+----------------+------------+--------------------------+---------------------------------------------------------------------------------------------------------+
    | Index | Name                                                 | Id                  | Priv_ip        | Size       | Launch_time              | Tags_txt                                                                                                |
    +-------+------------------------------------------------------+---------------------+----------------+------------+--------------------------+---------------------------------------------------------------------------------------------------------+
    | 1     | c01.mongo.dev.ec2.studyblue.com                      | i-091826d699b1eaa2c | 10.0.4.238     | t2.medium  | 2017-03-12T19:46:22.000Z | Role='mongoc', Env='development'                                                                        |
    | 2     | m11.s03.prod.ec2.studyblue.com                       | i-0cca166fda6666199 | 172.16.25.32   | r3.xlarge  | 2017-01-01T23:33:37.000Z | Role='mongod', Env='production'                                                                         |
    | 3     | webapp-i-066825b95336610e8.prod.ec2.studyblue.com    | i-066825b95336610e8 | 172.16.61.29   | m4.large   | 2017-03-31T21:20:01.000Z | Role='webapp', Env='production'                                                                         |
    | 4     | es-7.prod.ec2.studyblue.com                          | i-0d215827d8b600917 | 172.16.63.88   | r4.2xlarge | 2017-03-23T23:00:38.000Z | Role='elasticsearch', Env='production'                                                                  |
    | 5     | mongos.dev.ec2.studyblue.com                         | i-03fe546cd6aa9062b | 10.0.4.65      | t2.small   | 2017-03-12T19:46:29.000Z | Role='mongos', Env='development'                                                                        |
    | 6     | c2.mongo.prod.ec2.studyblue.com                      | i-00cdd42a86ba342ea | 172.16.24.171  | t2.medium  | 2016-12-31T00:38:58.000Z | Role='mongoc', Env='production'                                                                         |
    | 7     | es-6.prod.ec2.studyblue.com                          | i-0bb8c5320c5e8f8e6 | 172.16.63.212  | r4.2xlarge | 2017-03-23T23:00:44.000Z | Role='elasticsearch', Env='production'                                                                  |
    | 8     | generic-server.prod.ec2.studyblue.com                | i-00de213c6ee539f3f | 172.16.63.231  | t2.medium  | 2017-01-17T19:38:10.000Z | Role='generic-server', Env='production'                                                                 |
    | 9     | kibana-prod.prod.ec2.studyblue.com                   | i-05cab15eb13de7f1d | 172.16.63.132  | m4.large   | 2017-03-30T21:03:08.000Z | Role='kibana', Env='production'                                                                         |

Alternatively, you can search for any parameter in a fuzzy-match fashion:
::
    #> loony mongoc
    Searching for ['mongoc']
    +-------+---------------------------------+---------------------+---------------+-----------+--------------------------+----------------------------------+
    | Index | Name                            | Id                  | Priv_ip       | Size      | Launch_time              | Tags_txt                         |
    +-------+---------------------------------+---------------------+---------------+-----------+--------------------------+----------------------------------+
    | 1     | c1.mongo.prod.ec2.studyblue.com | i-00fb57e2d26c5996e | 172.16.24.36  | t2.medium | 2016-12-31T01:42:26.000Z | Role='mongoc', Env='production'  |
    | 2     | c03.mongo.dev.ec2.studyblue.com | i-033c1ae46d8ff4dcd | 10.0.4.248    | t2.medium | 2017-03-12T19:46:56.000Z | Role='mongoc', Env='development' |
    | 3     | c3.mongo.prod.ec2.studyblue.com | i-0fb60e4e3298898c4 | 172.16.25.131 | t2.medium | 2017-01-04T06:06:31.000Z | Role='mongoc', Env='production'  |
    | 4     | c2.mongo.prod.ec2.studyblue.com | i-00cdd42a86ba342ea | 172.16.24.171 | t2.medium | 2016-12-31T00:38:58.000Z | Role='mongoc', Env='production'  |
    | 5     | c01.mongo.dev.ec2.studyblue.com | i-091826d699b1eaa2c | 10.0.4.238    | t2.medium | 2017-03-12T19:46:22.000Z | Role='mongoc', Env='development' |
    | 6     | c02.mongo.dev.ec2.studyblue.com | i-0dec7789c46be02f5 | 10.0.4.109    | t2.medium | 2017-03-12T19:46:22.000Z | Role='mongoc', Env='development' |
    +-------+---------------------------------+---------------------+---------------+-----------+--------------------------+----------------------------------+


You can also search by keys for a more refined output:
::
    #> loony --keys
    The following keys are available:
    as_group_name, cfn_logical_id, cfn_stack_id, cfn_stack_name, env, id, launch_time, location, master, monitored, name, priv_dns, priv_ip, pub_dns, pub_ip, role, size, status, subnet_id, tags, tags_txt, vpc_id

    #> loony master=true
    Searching for ['master=true']
    +-------+--------------------------------+---------------------+---------------+-----------+--------------------------+------------------------------------------------+
    | Index | Name                           | Id                  | Priv_ip       | Size      | Launch_time              | Tags_txt                                       |
    +-------+--------------------------------+---------------------+---------------+-----------+--------------------------+------------------------------------------------+
    | 1     | m12.s04.prod.ec2.studyblue.com | i-0329996a5f1c2b7f7 | 172.16.25.142 | r3.xlarge | 2017-02-03T03:08:24.000Z | master='true', Role='mongod', Env='production' |
    +-------+--------------------------------+---------------------+---------------+-----------+--------------------------+------------------------------------------------+

    #> loony loony cfn_stack_name=mongo-prod-m12-s04
    Searching for ['cfn_stack_name=mongo-prod-m12-s04']
    +-------+--------------------------------+---------------------+---------------+-----------+--------------------------+------------------------------------------------+
    | Index | Name                           | Id                  | Priv_ip       | Size      | Launch_time              | Tags_txt                                       |
    +-------+--------------------------------+---------------------+---------------+-----------+--------------------------+------------------------------------------------+
    | 1     | m12.s04.prod.ec2.studyblue.com | i-0329996a5f1c2b7f7 | 172.16.25.142 | r3.xlarge | 2017-02-03T03:08:24.000Z | master='true', Role='mongod', Env='production' |
    +-------+--------------------------------+---------------------+---------------+-----------+--------------------------+------------------------------------------------+


You get the idea....
now how about the output? Well, fear not, it is customizable. There are a few builtins: --short and --long:
::
    #> loony --short cfn_stack_name=mongo-prod-m12-s04
    Searching for ['cfn_stack_name=mongo-prod-m12-s04']
    +-------+--------------------------------+---------------+---------+------------------------------------------------+
    | Index | Name                           | Priv_ip       | Status  | Tags_txt                                       |
    +-------+--------------------------------+---------------+---------+------------------------------------------------+
    | 1     | m12.s04.prod.ec2.studyblue.com | 172.16.25.142 | running | master='true', Role='mongod', Env='production' |
    +-------+--------------------------------+---------------+---------+------------------------------------------------+

    #> loony --long cfn_stack_name=mongo-prod-m12-s04
    Searching for ['cfn_stack_name=mongo-prod-m12-s04']
    +-------+--------------------------------+---------------------+---------------+--------+--------------+-----------------+-----------+------------+---------+-----------+--------------------------+------------+--------+--------+--------------------+
    | Index | Name                           | Id                  | Priv_ip       | Pub_ip | Vpc_id       | Subnet_id       | Size      | Location   | Status  | Monitored | Launch_time              | Env        | Role   | Master | Cfn_stack_name     |
    +-------+--------------------------------+---------------------+---------------+--------+--------------+-----------------+-----------+------------+---------+-----------+--------------------------+------------+--------+--------+--------------------+
    | 1     | m12.s04.prod.ec2.studyblue.com | i-0329996a5f1c2b7f7 | 172.16.25.142 |        | vpc-55c3dc30 | subnet-9ce4fba6 | r3.xlarge | us-east-1e | running | True      | 2017-02-03T03:08:24.000Z | production | mongod | true   | mongo-prod-m12-s04 |
    +-------+--------------------------------+---------------------+---------------+--------+--------------+-----------------+-----------+------------+---------+-----------+--------------------------+------------+--------+--------+--------------------+

You can of course also customize the output, using the same keys listed above:
::
    #> loony -o name,priv_ip cfn_stack_name=mongo-prod-m12-s04
    Searching for ['cfn_stack_name=mongo-prod-m12-s04']
    +--------------------------------+---------------+
    | Name                           | Priv_ip       |
    +--------------------------------+---------------+
    | m12.s04.prod.ec2.studyblue.com | 172.16.25.142 |
    +--------------------------------+---------------+

Finally, you can also combine things together:
::
    #> loony mongo size=t2.small env=production
    Searching for ['mongo', 'size=t2.small', 'env=production']
    +-------+--------------------------------+---------------------+---------------+----------+--------------------------+---------------------------------+
    | Index | Name                           | Id                  | Priv_ip       | Size     | Launch_time              | Tags_txt                        |
    +-------+--------------------------------+---------------------+---------------+----------+--------------------------+---------------------------------+
    | 1     | mongos.prod.ec2.studyblue.com  | i-0ab415ff7a0ef7b06 | 172.16.25.45  | t2.small | 2016-12-30T20:51:53.000Z | Role='mongos', Env='production' |
    | 2     | m03.s03.prod.ec2.studyblue.com | i-0a86af366f2167432 | 172.16.24.190 | t2.small | 2017-01-04T05:58:45.000Z | Role='mongoa', Env='production' |
    | 3     | m01.s01.prod.ec2.studyblue.com | i-0f57bbb64c4daf721 | 172.16.25.88  | t2.small | 2017-01-04T04:59:40.000Z | Role='mongoa', Env='production' |
    | 4     | m02.s02.prod.ec2.studyblue.com | i-0d672e48d49a264d3 | 172.16.25.217 | t2.small | 2017-01-04T04:59:39.000Z | Role='mongoa', Env='production' |
    +-------+--------------------------------+---------------------+---------------+----------+--------------------------+---------------------------------+

THAT's NOT ALL!
===============

Loony will also allow you to connect to the hosts it finds!
If there is only one result, it will ssh directly to it.
If there are more than 1 results, it will use tmux to connect to all the results, creating new virtual 'pages' in tmux parlance
depending on the number of servers to connect to.

To access this wonderful featuer, simply add -c to your loony command, or use the connect alias:
::
    #> connect jobserver-i-0b4b509cd8e988144.prod.ec2.studyblue.com
    Searching for ['jobserver-i-0b4b509cd8e988144.prod.ec2.studyblue.com']
    +-------+------------------------------------------------------+---------------------+---------------+----------+--------------------------+------------------------------------+
    | Index | Name                                                 | Id                  | Priv_ip       | Size     | Launch_time              | Tags_txt                           |
    +-------+------------------------------------------------------+---------------------+---------------+----------+--------------------------+------------------------------------+
    | 1     | jobserver-i-0b4b509cd8e988144.prod.ec2.studyblue.com | i-0b4b509cd8e988144 | 172.16.61.241 | m4.large | 2017-03-31T21:06:25.000Z | Role='jobserver', Env='production' |
    +-------+------------------------------------------------------+---------------------+---------------+----------+--------------------------+------------------------------------+
    choices of 1 instances
    Note: make sure you are connected to the VPN!
    Connecting to 172.16.61.241
    Last login: Mon Apr  3 09:52:06 2017 from 192.168.150.144

            __|  __|_  )
            _|  (     /   Amazon Linux AMI
            ___|\___|___|

    https://aws.amazon.com/amazon-linux-ami/2016.09-release-notes/
    [fred@jobserver-i-0b4b509cd8e988144 ~]$

And for more than one server:
::
    #> loony -c jobserver env=production
    fatal: No names found, cannot describe anything.
    Searching for ['jobserver', 'env=production']
    +-------+------------------------------------------------------+---------------------+---------------+----------+--------------------------+------------------------------------+
    | Index | Name                                                 | Id                  | Priv_ip       | Size     | Launch_time              | Tags_txt                           |
    +-------+------------------------------------------------------+---------------------+---------------+----------+--------------------------+------------------------------------+
    | 1     | jobserver-i-0b4b509cd8e988144.prod.ec2.studyblue.com | i-0b4b509cd8e988144 | 172.16.61.241 | m4.large | 2017-03-31T21:06:25.000Z | Role='jobserver', Env='production' |
    | 2     | jobserver-i-087b42a77af762531.prod.ec2.studyblue.com | i-087b42a77af762531 | 172.16.63.6   | m4.large | 2017-03-31T21:35:28.000Z | Role='jobserver', Env='production' |
    | 3     | jobserver-i-05c20794cbb8e6d99.prod.ec2.studyblue.com | i-05c20794cbb8e6d99 | 172.16.63.147 | m4.large | 2017-03-31T21:35:28.000Z | Role='jobserver', Env='production' |
    | 4     | jobserver-i-01806f3d6648812a7.prod.ec2.studyblue.com | i-01806f3d6648812a7 | 172.16.61.223 | m4.large | 2017-04-01T07:40:15.000Z | Role='jobserver', Env='production' |
    | 5     | jobserver-i-014765598b8d86349.prod.ec2.studyblue.com | i-014765598b8d86349 | 172.16.61.48  | m4.large | 2017-03-31T21:06:25.000Z | Role='jobserver', Env='production' |
    | 6     | jobserver-i-080d1ed6835388eb0.prod.ec2.studyblue.com | i-080d1ed6835388eb0 | 172.16.61.240 | m4.large | 2017-03-31T20:58:35.000Z | Role='jobserver', Env='production' |
    +-------+------------------------------------------------------+---------------------+---------------+----------+--------------------------+------------------------------------+
    choices of 6 instances


.. image:: tmux.png

Also you can run a command on all the server instances that are returned
::
    #> loony --cmd 'ps auxw | grep tomcat' role=webapp env=production

If you want to run commands serially on a multitude of servers without using tmux (ie: non-interactively):
::
    #> loony --cmd 'ps auxw | grep tomcat' -b role=webapp env=production

**NOTE:** if you pass 'logs' as the command, it will start tailing logs, based on list of dict defined in connect.py and/or system logs.

INSTALL
=======
Installing those scripts is a pip command away!
This command will do the trick:
::
    #> sudo pip install loony


(don't use sudo if you are in a virtualenv, but the script will then only be available when in that virtualenv...)

One could also clone the repo and run
::
    #> git clone ssh://git@github.com/StudyBlue/loony.git
    #> cd loony
    #> python setup.py install


Finally, you can use the Binary version (note: connect will not be aliased and loony -c will need to be used instead). 

Download the binary from `https://github.com/StudyBlue/loony/blob/master/dist/loony <https://github.com/StudyBlue/loony/blob/master/dist/loony>`_

SETUP
=====
In order to work ~/.aws/credentials needs to be setup. This is the same file that aws-cli and boto use. It should look
similar to this:
::
    [default]
    region = us-east-1
    aws_access_key_id = blahblah
    aws_secret_access_key = blahblah
    output = text

    [prod]
    region = us-east-1
    aws_access_key_id = blahblah
    aws_secret_access_key = blahblah
    output = text

I usually set [default] like [prod]

Next, edit setting.py (depending on how you installed the script, the location will vary)
If you install it from pip without virtualenv, it will be in /Library/Python/2.7/site-packages/loony/settings.py

Based on your credentials, you might want to adjust the default_aws_domains variable. (yes, I am working on making
this a dotfile in your homedir)

USAGE
=====

The installer will setup two scripts:

- loony  => used for searching for things

- connect => used to connect to things

The two essentially work the exact same way, but connect will offer a prompt after displaying the list of machines
for you to choose which one to connect to.
::
    #> loony --help
    usage: main.py [-h] [-v] [-d] [--short] [--long] [--nocache] [-k] [--version]
                    [-o [OUTPUT]] [-u [USER]] [-c] [-b] [-1] [--cmd [CMD]]
                    [search [search ...]]
    Find stuff in AWS
    positional arguments:
        search                Search parameters
    optional arguments:
        -h, --help            show this help message and exit
        -v, --verbose         Increase log verbosity
        -d, --debug           Debug level verbosity
        --short               Display short-format results
        --long                Display long-format results
        -nc, --nocache             Force cache expiration
        -k, --keys            List all the keys for indexing or output
        --version             Print version
        -o [OUTPUT], --out [OUTPUT]   Output format eg. id,name,pub_ip
        -u [USER], --user [USER]  When connecting, what user to ssh in as
        -c, --connect         Connect to one or more instances
        -b, --batch           Batch mode. Won't use tmux to run cmd
        -1                    connect to only one of the result instances (choice)
        --cmd [CMD]           Run this command on resulting hosts


ADVANCED STUFF
==============

Creating a binary... You can create a loony binary out of the source code, so that loony can be used on systems with old or no python installed.
To create the binary, you need pyinstaller (pip).
::
    #> pyinstaller loony/main.py --onefile --clean -p ./loony -n loony

Once the binary is build, it can be placed in /usr/local/bin, which is done by install.sh.

Note: when running loony this way, 'connect' will not be available, so you will have to use 'loony -c' instead