=====
Loony
=====

This script allows for querying AWS to find the right resources when you need them.


INSTALL
=======
Installing those scripts is a pip command away!
Sadly, Bitbucket SSL is somehow troubling to BitBucket...
Anyway, this command will do the trick:

sudo pip install https://github.com/azafred/loony/archive/master.zip
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

