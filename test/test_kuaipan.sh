#!/bin/sh
NETDISK="python ../netdisk_cli"
APP_TOKEN='xcbjepsPi1sbTBJh|GKW0dvIwWrnyAYXt'
USER_TOKEN='000bd98a45e8b717b001d834|be7c24c6de9640f08d45a02289dcf9e0'

echo "==== Version ===="
$NETDISK --version

echo "==== info ===="
$NETDISK -n kuaipan -a $APP_TOKEN \
    -u $USER_TOKEN \
    info  

echo "==== ls ===="
$NETDISK -n kuaipan -a $APP_TOKEN \
    -u $USER_TOKEN \
    ls / 

echo "==== put ===="
$NETDISK -n kuaipan -a $APP_TOKEN \
    -u $USER_TOKEN \
    put test_kuaipan.sh test/t.sh

echo "==== cat ===="
$NETDISK -n kuaipan -a $APP_TOKEN \
    -u $USER_TOKEN \
    cat test/t.sh

echo "==== mv ===="
$NETDISK -n kuaipan -a $APP_TOKEN \
    -u $USER_TOKEN \
    mv test/t.sh test2/a.sh 

echo "==== put a.sh ===="
$NETDISK -n kuaipan -a $APP_TOKEN \
    -u $USER_TOKEN \
    put test_kuaipan.sh test/a.sh


echo "==== ls ===="
$NETDISK -n kuaipan -a $APP_TOKEN \
    -u $USER_TOKEN \
    ls test

echo "==== copy ===="
$NETDISK -n kuaipan -a $APP_TOKEN \
    -u $USER_TOKEN \
    cp test/a.sh test/b.sh


echo "==== rm ===="
$NETDISK -n kuaipan -a $APP_TOKEN \
    -u $USER_TOKEN \
    rm test

echo "==== ls ===="
$NETDISK -n kuaipan -a $APP_TOKEN \
    -u $USER_TOKEN \
    ls  


