#!/bin/sh

cmd="python ../netdisk.py"
apptoken='xcbjepsPi1sbJh|GKWvIwWrnyAYXt'
usertoken='000bd98a45e717c3516fda|35f806af45dd99c4d58da8499536'

echo "==== Version ===="
$cmd --version

echo "==== info ===="
$cmd -n kuaipan -a $apptoken \
    -u $usertoken \
    info  

echo "==== ls ===="
$cmd -n kuaipan -a $apptoken \
    -u $usertoken \
    ls / 

echo "==== put ===="
$cmd -n kuaipan -a $apptoken \
    -u $usertoken \
    put test_kuaipan.sh test/t.sh

echo "==== cat ===="
$cmd -n kuaipan -a $apptoken \
    -u $usertoken \
    cat test/t.sh

echo "==== mv ===="
$cmd -n kuaipan -a $apptoken \
    -u $usertoken \
    mv test/t.sh test2/a.sh 

echo "==== put a.sh ===="
$cmd -n kuaipan -a $apptoken \
    -u $usertoken \
    put test_kuaipan.sh test/a.sh


echo "==== ls ===="
$cmd -n kuaipan -a $apptoken \
    -u $usertoken \
    ls test

echo "==== copy ===="
$cmd -n kuaipan -a $apptoken \
    -u $usertoken \
    cp test/a.sh test/b.sh


echo "==== rm ===="
$cmd -n kuaipan -a $apptoken \
    -u $usertoken \
    rm test

echo "==== ls ===="
$cmd -n kuaipan -a $apptoken \
    -u $usertoken \
    ls  


