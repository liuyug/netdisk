#!/bin/sh

NETDISK="python ../netdisk_cli"
APP_TOKEN='xcbjepsPi1sbTBJh|GKW0dvIwWrnyAYXt'
USER_TOKEN='000bd98a45e8b717b001d834|be7c24c6de9640f08d45a02289dcf9e0'


echo "==== ask_token ===="
$NETDISK -n kuaipan -a $APP_TOKEN ask 

#echo "==== copy_ref ===="
#../netdisk_cli.py -n kuaipan -a $APP_TOKEN \
#    -u $USER_TOKEN \
#    cp test_copy.sh b.sh


