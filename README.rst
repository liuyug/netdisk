=============
NetDisk
=============

网盘的命令行接口, 支持以下网盘:

+ Dropbox

  下载 `Dropbox API <https://www.dropbox.com/developers>`_

命令行格式
==========

Usage::

    Usage: netdisk_cli.py [options] command [argument ...]
    
    Commands: ask, put, get, ls, rm, mv, info, cp
    
    Options:
      -h, --help    show this help message and exit
      -q, --quiet   don't print status messages to stdout
      -n NETDISK    netdisk type: dropbox
      -a APPTOKEN   netdisk app token
      -u USERTOKEN  user access token
    
    Sample: netdisk_cli.py -a apptoken -u usertoken ls

Sample::

    # 申请一个新的用户token
    netdisk_cli.py -a apptoken ask
    # 查看目录
    netdisk_cli.py -a apptoken -u usertoken ls

