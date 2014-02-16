=============
NetDisk
=============

|version| |download|

网盘的命令行接口, 支持以下网盘:

+ Dropbox
+ Kuaipan

命令行格式
==========
::

    usage: netdisk.py [-h] [--version] [-v] [--listdisk] [--d1 DISKNAME1]
                      [--d2 DISKNAME2] [-n TYPE] [-a APPTOKEN] [-u USERTOKEN]
                      [-d DESTTOKEN]
                      [command] [path [path ...]]

    Module:
        dropbox: 1.5.1
        kuaipan: 0.1beta

    positional arguments:
      command         Support: info, put, mv, ls, get, ask, rm, cp, cat
      path            directory or files

    optional arguments:
      -h, --help      show this help message and exit
      --version       show program's version number and exit
      -v, --verbose   verbose help
      --listdisk      list netdisk name in config
      --d1 DISKNAME1  netdisk name in config
      --d2 DISKNAME2  netdisk name in config, the destination in command cp
      -n TYPE         netdisk type: dropbox, kuaipan
      -a APPTOKEN     netdisk app token
      -u USERTOKEN    user access token
      -d DESTTOKEN    destination user access token, for copy between two users

API
=====
1. `Dropbox API <https://www.dropbox.com/developers>`_
2. `Kuapan API <http://www.kuaipan.cn/developers/document.htm>`_

.. |version| image:: http://img.shields.io/pypi/v/netdisk.svg
    :target: https://pypi.python.org/pypi/netdisk/
    :alt: Version

.. |download| image:: http://img.shields.io/pypi/dm/netdisk.svg
    :target: https://pypi.python.org/pypi/netdisk/
    :alt: Downloads
