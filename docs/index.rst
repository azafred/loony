
=====
Loony
=====

This script allows for querying AWS to find the right resources when you need them.
In essence, if you want to find what that machine with the IP 10.20.60.137 is, well, you can't use DNS and logging in AWS takes too long.
but...
::
    #> loony 10.20.60.137
    Searching for ['10.20.60.137']
    +-------+--------+--------------------------------------+------------+--------------+----------------+--------------+-----------------+-----------+------------+---------+-----------+-----------+--------+------------+
    | Index | Pillar | Name                                 | Id         | Priv_ip      | Pub_ip         | Vpc_id       | Subnet_id       | Size      | Location   | Status  | Monitored | Sc_pillar | Sc_app | Sc_version |
    +-------+--------+--------------------------------------+------------+--------------+----------------+--------------+-----------------+-----------+------------+---------+-----------+-----------+--------+------------+
    | 1     | prod   | (Production) HaProxy Node 2 (galera) | i-77fbe68a | 10.20.60.137 | 54.210.168.142 | vpc-9450f0f1 | subnet-fe077c89 | m3.xlarge | us-east-1b | running | True      |           |        |            |
    +-------+--------+--------------------------------------+------------+--------------+----------------+--------------+-----------------+-----------+------------+---------+-----------+-----------+--------+------------+

Many things can be searched for, and search items can be combined:
::
    #> loony --short vpc-07193060 subnet-7901c422
    Searching for ['vpc-07193060', 'subnet-7901c422']
    +-------+------------------------------------------------------------+--------------+---------+
    | Index | Name                                                       | Priv_ip      | Status  |
    +-------+------------------------------------------------------------+--------------+---------+
    | 1     | ECS Instance - EC2ContainerService-exp-jenkins-build-nodes | 10.105.62.25 | running |
    | 2     | exp-consul-ue1d-00                                         | 10.105.53.63 | stopped |
    +-------+------------------------------------------------------------+--------------+---------+

The output can also be customized:
::
    #> loony -o index,name,vpc_id,priv_ip  vpc-07193060 subnet-7901c422
    Searching for ['vpc-07193060', 'subnet-7901c422']
    +-------+------------------------------------------------------------+--------------+--------------+
    | Index | Name                                                       | Vpc_id       | Priv_ip      |
    +-------+------------------------------------------------------------+--------------+--------------+
    | 1     | ECS Instance - EC2ContainerService-exp-jenkins-build-nodes | vpc-07193060 | 10.105.62.25 |
    | 2     | exp-consul-ue1d-00                                         | vpc-07193060 | 10.105.53.63 |
    +-------+------------------------------------------------------------+--------------+--------------+


*By default, the search items will be joined with and implicit AND. Sometimes you might want to OR them however...*
::
    #> loony --or -o index,name,vpc_id,priv_ip  vpc-07193060 subnet-7901c422
    Searching for ['vpc-07193060', 'subnet-7901c422']
    +-------+------------------------------------------------------------+--------------+---------------+
    | Index | Name                                                       | Vpc_id       | Priv_ip       |
    +-------+------------------------------------------------------------+--------------+---------------+
    | 1     | exp-consul-ue1b-00                                         | vpc-07193060 | 10.105.23.49  |
    | 2     | ECS Instance - EC2ContainerService-exp-jenkins-build-nodes | vpc-07193060 | 10.105.35.6   |
    | 3     | ECS Instance - EC2ContainerService-exp-jenkins-build-nodes | vpc-07193060 | 10.105.62.25  |
    | 4     | exp-jenkins-seth-1                                         | vpc-07193060 | 10.105.19.96  |
    | 5     | exp-bastion                                                | vpc-07193060 | 10.105.1.145  |
    | 6     | exp-consul-ue1d-00                                         | vpc-07193060 | 10.105.53.63  |
    | 7     | exp-mongo-cassandra                                        | vpc-07193060 | 10.105.33.121 |
    | 8     | exp-consul-ue1c-00                                         | vpc-07193060 | 10.105.35.45  |
    | 9     | exp-jenkins-seth-2                                         | vpc-07193060 | 10.105.18.191 |
    +-------+------------------------------------------------------------+--------------+---------------+

INSTALL
=======
Installing those scripts is a pip command away!
Sadly, Bitbucket SSL is somehow troubling to BitBucket...
Anyway, this command will do the trick:

sudo pip install https://github.com/azafred/loony/archive/master.zip

or

sudo pip install  https://bitbucket.sparkcentral.ninja:7999/int/loony.git/archive/master.zip

(don't use sudo if you are in a virtualenv, but the script will then only be available when in that virtualenv...)

One could also clone the repo and run

git clone ssh://git@bitbucket.sparkcentral.ninja:7999/int/loony.git
cd loony
python setup.py install


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

    [fred]
    region = us-west-1
    aws_access_key_id = blahblah
    aws_secret_access_key = blahblah
    output = text

    [prod]
    region = us-east-1
    aws_access_key_id = blahblah
    aws_secret_access_key = blahblah
    output = text

    [qa]
    region = us-east-1
    aws_access_key_id = blahblah
    aws_secret_access_key = blahblah
    output = text

    [ops]
    region = us-east-1
    aws_access_key_id = blahblah
    aws_secret_access_key = blahblah
    output = text


    [experiments]
    region = us-east-1
    aws_access_key_id = blahblah
    aws_secret_access_key = blahblah
    output = text


I usually set [default] like [prod]

Next, edit setting.py (depending on how you installed the script, the location will vary)
If you install it from pip without virtualenv, it will be in /Library/Python/2.7/site-packages/loony/settings.py

Based on your credentials, you might want to adjust the default_aws_domains variable.

USAGE
=====

The installer will setup two scripts:

- loony  => used for searching for things

- connect => used to connect to things

The two essentially work the exact same way, but connect will offer a prompt after displaying the list of machines
for you to choose which one to connect to.

::
    #> loony --help
    usage: loony [-h] [-v] [-d] [-la] [-so] [-ro] [-pub] [--short] [--nocache]
                 [--or] [-o [OUTPUT]]
                 [search [search ...]]

    Find stuff in AWS

    positional arguments:
      search                Search parameters

    optional arguments:
      -h, --help            show this help message and exit
      -v, --verbose         Increase log verbosity
      -d, --debug           Debug level verbosity
      -la, --list-all       List all instances
      -so, --stopped        Only display stopped instances
      -ro, --running        Only display running instances
      -pub, --public        Find those instances with public IPs
      --short               Display short-format results
      --nocache             Force cache expiration
      --or                  Search item OR instead of combined
      -o [OUTPUT], --out [OUTPUT]
                        Output format eg. id,name,pub_ip
::