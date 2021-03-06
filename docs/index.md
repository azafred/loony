---
layout: default
---
Welcome to Loony's homepage.

Loony is a command line tool designed to help you find instances and potentially connect to them.

The tool was (badly) written in python, and is hosted on github (See links above) 
<HR>
# Requirements:
If you are using the binary version, there are no other requirements. However, the best experience will be had if you are using iterm and have tmux installed (```brew install tmux```)

If you are using the python version (from source, or from pip), you will need to have python 2.7 installed, as well as all the packages listed in the requires.txt file (```pip install -r requirements.txt```)

<HR>
# Installation:
## Binaries:
Binaries for both MacOS and Linux are hosted on S3. 

To install the binaries, simply run the following command: 

On a mac:
```bash
$> wget https://s3.amazonaws.com/studyblue-binaries/loony_macos_latest -O /usr/local/bin/loony && chmod 755 $_
```

On Linux:
```bash
$> wget https://s3.amazonaws.com/studyblue-binaries/loony_linux_latest -O /usr/local/bin/loony && chmod 755 $_
```

Of course, for this to work, you will also have to make sure ```/usr/local/bin``` is in your path.

Additionally, it would be usefull to setup a few aliases. For simplicity's sake, here is what I would suggest:
```bash
PATH=$PATH:/usr/local/bin
alias l='loony'
alias c='loony -c'
```
## Pip:
pip is the standard way of distributing python modules. Sadly, it is not always easy to get to work. However, it will be more integrated in the python ecosystem, should you ever want to import loony or some of its parts into your own project.

Simply run the following to install in your main python distribution. You can of course customize this to work with virtualenv... I'll leave this exercise to the reader... 

```bash
$> sudo pip install loony
```

This command will automatically install ```/usr/local/bin/loony``` and ```/usr/local/bin/connect```. 
## Source:
Finally, you can checkout the source repo and install loony from it:

```bash
$> git clone git@github.com:StudyBlue/loony.git
$> cd loony
$> python setup.py install
```
This commands will automatically install ```/usr/local/bin/loony``` and ```/usr/local/bin/connect```. 
<HR>

# Setup:

In order to work ```~/.aws/credentials``` needs to be setup. This is the same file that aws-cli and boto use. It should look
similar to this:
```
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
```
I usually set [default] the same way as [prod]

<HR>

# Usage:
```
usage: loony [-h] [-v] [-d] [--short] [--long] [-nc] [-k] [--version]
          [-o [OUTPUT]] [-u [USER]] [-c] [-p] [-b] [-nt] [-1] [--cmd [CMD]]
          [-or [orsearch [orsearch ...]]] [--upgrade]
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
  -nc, --nocache        Force cache expiration
  -k, --keys            List all the keys for indexing or output
  --version             Print version
  -o [OUTPUT], --out [OUTPUT]
                        Output format eg. id,name,pub_ip
  -u [USER], --user [USER]
                        When connecting, what user to ssh in as
  -c, --connect         Connect to one or more instances
  -p, --public          Connect via public IP instead.
  -b, --batch           Batch mode. Won't use tmux to run cmd
  -nt, --notable        Don't print an ascii table
  -1                    connect to only one of the result instances (choice)
  --cmd [CMD]           Run this command on resulting hosts
  -or [orsearch [orsearch ...]], --or [orsearch [orsearch ...]]
                        things to or in a search
  --upgrade             upgrade Loony
```

<HR>

# Examples:
In its simplest form, loony will simply return all the hosts running in AWS:

```
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
```
Alternatively, you can search for any parameter in a fuzzy-match fashion:
```
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
```

You can also search by keys for a more refined output:
```
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
```

You get the idea....
now how about the output? Well, fear not, it is customizable. There are a few builtins: --short and --long:
```
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
```
You can of course also customize the output, using the same keys listed above:
```
#> loony -o name,priv_ip cfn_stack_name=mongo-prod-m12-s04
Searching for ['cfn_stack_name=mongo-prod-m12-s04']
+--------------------------------+---------------+
| Name                           | Priv_ip       |
+--------------------------------+---------------+
| m12.s04.prod.ec2.studyblue.com | 172.16.25.142 |
+--------------------------------+---------------+
```
You can also get details on devstacks with the following handy dandy one:
```
#> loony devstack
Searching for ['devstack']
Cache set to expire on 2017-12-23 15:16:28.665622
Checking for changes...
No changes detected. Using cache.
+-------+-------------------------------------------------+-----------------+---------+----------------------------------------------------+-----------+---------------+---------------------------+
| Index | Name                                            | Priv_ip         | Bigdata | Branch                                             | Es_status | Rev           | Launch_time               |
+-------+-------------------------------------------------+-----------------+---------+----------------------------------------------------+-----------+---------------+---------------------------+
| 1     | devstack-web-arya.dev.ec2.studyblue.com         | 172.16.105.212  | false   | www-arya                                           | green     | 13-1-r3dev    | 2017-08-02T19:42:43.000Z  |
| 2     | devstack-web-nymeria.dev.ec2.studyblue.com      | 10.0.0.77       | True    | release-12.41.11                                   | green     | 12-41-r10dev  | 2017-10-24T18:10:30.000Z  |
| 3     | devstack-web-excelsior.dev.ec2.studyblue.com    | 10.0.4.111      | false   | develop                                            | green     | 13-1-r1dev    | 2017-11-14T18:39:59.000Z  |
| 4     | devstack-web-antares.dev.ec2.studyblue.com      | 10.0.4.11       | false   | develop                                            | green     | 13-1-r1dev    | 2017-11-14T18:44:15.000Z  |
| 5     | devstack-web-ajax.dev.ec2.studyblue.com         | 10.0.4.213      | false   | develop                                            | green     | 13-1-r1dev    | 2017-11-14T18:47:12.000Z  |
| 6     | devstack-web-titan.dev.ec2.studyblue.com        | 10.0.4.221      | false   | develop                                            | green     | 13-1-r53dev   | 2017-11-29T00:20:05.000Z  |
| 7     | devstack-web-riker.dev.ec2.studyblue.com        | 10.0.4.66       | True    | CORE-772                                           | green     | 13-1-r5dev    | 2017-12-05T17:14:57.000Z  |
| 8     | devstack-web-enterprise.dev.ec2.studyblue.com   | 10.0.4.131      | True    | IOS-4830-Recommended-materials-class-and-homepage  | green     | 13-1-r1dev    | 2017-12-07T20:27:01.000Z  |
| 9     | devstack-web-tyrion.dev.ec2.studyblue.com       | 10.0.4.109      | True    | SUM-373_Update_UX_Pagination                       | green     | 13-1-r2dev    | 2017-12-11T20:24:13.000Z  |
| 10    | devstack-web-ludo.dev.ec2.studyblue.com         | 10.0.4.149      | false   | CORE-940_TextbookInOnboarding                      | green     | 13-1-r1dev    | 2017-12-11T23:51:25.000Z  |
| 11    | devstack-web-yoda.dev.ec2.studyblue.com         | 10.0.4.103      | True    | ts-15                                              | green     | 13-1-r1dev    | 2017-12-12T22:51:21.000Z  |
| 12    | devstack-web-ashitaka.dev.ec2.studyblue.com     | 10.0.4.101      | false   | CORE-1032-land-on-deck                             | red       | 13-1-r5dev    | 2017-12-14T00:58:03.000Z  |
| 13    | devstack-web-rakibul.dev.ec2.studyblue.com      | 172.16.105.243  | false   | CORE-930_AddDepartment_api                         | green     | 13-1-r1dev    | 2017-12-14T17:42:41.000Z  |
| 14    | devstack-web-krakatoa.dev.ec2.studyblue.com     | 10.0.4.125      | True    | Core-1050_ColorChangesProAwareness                 | green     | 13-1-r2dev    | 2017-12-15T07:42:27.000Z  |
| 15    | devstack-web-voyager.dev.ec2.studyblue.com      | 10.0.4.107      | True    | CORE-996_Limit_HWH_searches                        | red       | 13-1-r7dev    | 2017-12-18T18:30:03.000Z  |
| 16    | devstack-web-melkor.dev.ec2.studyblue.com       | 10.0.4.182      | True    | Core-1050_ColorChangesProAwareness                 | green     | 13-1-r2dev    | 2017-12-20T00:32:23.000Z  |
| 17    | devstack-web-kasthurim.dev.ec2.studyblue.com    | 10.0.4.237      | false   | TS-5-tbs-introduction-screen                       | red       | 13-1-r2dev    | 2017-12-20T00:32:26.000Z  |
| 18    | devstack-web-riviere.dev.ec2.studyblue.com      | 10.0.4.171      | false   | CORE-829_lihpStylingChanges                        | green     | 13-1-r3dev    | 2017-12-20T18:36:12.000Z  |
| 19    | devstack-web-chewbacca.dev.ec2.studyblue.com    | 10.0.4.133      | True    | Core-1034_StarringCardsCosmeticChanges             | green     | 13-1-r1dev    | 2017-12-20T22:42:09.000Z  |
| 20    | devstack-web-hermione.dev.ec2.studyblue.com     | 10.0.4.37       | false   | CORE-996_Limit_HWH_searches                        | green     | 13-1-r18dev   | 2017-12-21T01:35:57.000Z  |
| 21    | devstack-web-galatea.dev.ec2.studyblue.com      | 10.0.4.4        | True    | SUM-373_Update_UX_Pagination                       | red       | 13-1-r1dev    | 2017-12-21T06:36:57.000Z  |
| 22    | devstack-web-defiant.dev.ec2.studyblue.com      | 10.0.4.217      | True    | SUM-786_remove-date-link                           | green     | 13-1-r1dev    | 2017-12-21T06:55:40.000Z  |
| 23    | devstack-web-trenzalore.dev.ec2.studyblue.com   | 10.0.4.25       | True    | CORE-1053_ChapterFinder                            | red       | 13-1-r2dev    | 2017-12-21T18:23:49.000Z  |
| 24    | devstack-web-jarjar.dev.ec2.studyblue.com       | 10.0.4.15       | True    | texsol                                             | green     | 13-1-r16dev   | 2017-12-21T19:05:33.000Z  |
| 25    | devstack-web-tardis.dev.ec2.studyblue.com       | 10.0.4.59       | True    | CORE-829_lihpStylingChanges                        | green     | 13-1-r1dev    | 2017-12-21T19:24:24.000Z  |
| 26    | devstack-web-dory.dev.ec2.studyblue.com         | 10.0.4.110      | True    | CORE-804_email-verification                        | green     | 13-1-r4dev    | 2017-12-21T21:07:40.000Z  |
| 27    | devstack-web-firefly.dev.ec2.studyblue.com      | 10.0.4.130      | True    | CORE-939_Textbook_Onboarding_SeoDeck               | green     | 13-1-r6dev    | 2017-12-21T21:24:58.000Z  |
| 28    | devstack-web-rhea.dev.ec2.studyblue.com         | 10.0.4.178      | True    | SUM-713_class-professor-deep-link                  | green     | 13-1-r1dev    | 2017-12-21T21:49:09.000Z  |
| 29    | devstack-web-devi.dev.ec2.studyblue.com         | 10.0.4.204      | True    | SUM-767_Update_queries_SEO_pages                   | red       | 13-1-r4dev    | 2017-12-21T22:31:34.000Z  |
| 30    | devstack-web-mantastic.dev.ec2.studyblue.com    | 10.0.4.12       | True    | IOS-4830-Recommended-materials-class-and-homepage  | green     | 13-1-r1dev    | 2017-12-21T22:32:20.000Z  |
| 31    | devstack-web-optimus.dev.ec2.studyblue.com      | 10.0.4.52       | True    | CORE-804_email-verification                        | green     | 13-1-r2dev    | 2017-12-21T23:23:40.000Z  |
| 32    | devstack-web-hood.dev.ec2.studyblue.com         | 10.0.4.161      | false   | CORE-885-masonry-load-flowed-redo                  | green     | 13-1-r3dev    | 2017-12-21T23:47:20.000Z  |
| 33    | devstack-web-dianaprince.dev.ec2.studyblue.com  | 10.0.4.244      | True    | CORE-804_email-verification                        | green     | 13-1-r1dev    | 2017-12-21T23:54:40.000Z  |
| 34    | devstack-web-direwolf.dev.ec2.studyblue.com     | 10.0.4.64       | false   | CORE-804_email-verification                        | green     | 13-1-r1dev    | 2017-12-22T01:37:08.000Z  |
| 35    | devstack-web-mobile.dev.ec2.studyblue.com       | 172.16.105.196  | false   | develop                                            | green     | 13-1-r191dev  | 2017-12-22T13:13:34.000Z  |
| 36    | devstack-web-hogwarts.dev.ec2.studyblue.com     | 10.0.4.67       | True    | develop                                            | green     | 13-1-r20dev   | 2017-12-22T18:57:08.000Z  |
| 37    | devstack-web-develop.dev.ec2.studyblue.com      | 10.0.4.232      | True    | develop                                            | green     | 13-1-r269dev  | 2017-12-22T20:16:05.000Z  |
+-------+-------------------------------------------------+-----------------+---------+----------------------------------------------------+-----------+---------------+---------------------------+
```
Finally, you can also combine things together:
```
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
```
## THAT's NOT ALL!

Loony will also allow you to connect to the hosts it finds!
If there is only one result, it will ssh directly to it.
If there are more than 1 results, it will use tmux to connect to all the results, creating new virtual 'pages' in tmux parlance
depending on the number of servers to connect to.

To access this wonderful featuer, simply add -c to your loony command, or use the connect alias:
```
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
```
And for more than one server:
```
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
```

![Helpful screenshot]({{ "/assets/tmux.png" | absolute_url }})


Also you can run a command on all the server instances that are returned
```
#> loony --cmd 'ps auxw | grep tomcat' role=webapp env=production
```
If you want to run commands serially on a multitude of servers without using tmux (ie: non-interactively):
```
#> loony --cmd 'ps auxw | grep tomcat' -b role=webapp env=production
```
**NOTE:** if you pass 'logs' as the command, it will start tailing logs, based on list of dict defined in connect.py and/or system logs.

<HR>

