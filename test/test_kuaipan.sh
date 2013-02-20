#!/bin/sh
echo "==== Version ===="
../netdisk_cli.py --version

echo "==== info ===="
../netdisk_cli.py -n kuaipan -a 'xcbjepsPi1sbTBJh|GKW0dvIwWrnyAYXt' \
    -u '000bd98a45e8b717b001d834|be7c24c6de9640f08d45a02289dcf9e0' \
    info  

echo "==== ls ===="
../netdisk_cli.py -n kuaipan -a 'xcbjepsPi1sbTBJh|GKW0dvIwWrnyAYXt' \
    -u '000bd98a45e8b717b001d834|be7c24c6de9640f08d45a02289dcf9e0' \
    ls / 

echo "==== put ===="
../netdisk_cli.py -n kuaipan -a 'xcbjepsPi1sbTBJh|GKW0dvIwWrnyAYXt' \
    -u '000bd98a45e8b717b001d834|be7c24c6de9640f08d45a02289dcf9e0' \
    put test_kuaipan.sh test/t.sh

echo "==== cat ===="
../netdisk_cli.py -n kuaipan -a 'xcbjepsPi1sbTBJh|GKW0dvIwWrnyAYXt' \
    -u '000bd98a45e8b717b001d834|be7c24c6de9640f08d45a02289dcf9e0' \
    cat test/t.sh

echo "==== mv ===="
../netdisk_cli.py -n kuaipan -a 'xcbjepsPi1sbTBJh|GKW0dvIwWrnyAYXt' \
    -u '000bd98a45e8b717b001d834|be7c24c6de9640f08d45a02289dcf9e0' \
    mv test/t.sh test2/a.sh 

echo "==== put a.sh ===="
../netdisk_cli.py -n kuaipan -a 'xcbjepsPi1sbTBJh|GKW0dvIwWrnyAYXt' \
    -u '000bd98a45e8b717b001d834|be7c24c6de9640f08d45a02289dcf9e0' \
    put test_kuaipan.sh test/a.sh


echo "==== ls ===="
../netdisk_cli.py -n kuaipan -a 'xcbjepsPi1sbTBJh|GKW0dvIwWrnyAYXt' \
    -u '000bd98a45e8b717b001d834|be7c24c6de9640f08d45a02289dcf9e0' \
    ls test

echo "==== copy ===="
../netdisk_cli.py -n kuaipan -a 'xcbjepsPi1sbTBJh|GKW0dvIwWrnyAYXt' \
    -u '000bd98a45e8b717b001d834|be7c24c6de9640f08d45a02289dcf9e0' \
    cp test/a.sh test/b.sh


echo "==== rm ===="
../netdisk_cli.py -n kuaipan -a 'xcbjepsPi1sbTBJh|GKW0dvIwWrnyAYXt' \
    -u '000bd98a45e8b717b001d834|be7c24c6de9640f08d45a02289dcf9e0' \
    rm test

echo "==== ls ===="
../netdisk_cli.py -n kuaipan -a 'xcbjepsPi1sbTBJh|GKW0dvIwWrnyAYXt' \
    -u '000bd98a45e8b717b001d834|be7c24c6de9640f08d45a02289dcf9e0' \
    ls  


