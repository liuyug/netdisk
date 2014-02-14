=============
NetDisk
=============

网盘的命令行接口, 支持以下网盘:

+ Dropbox
+ Kuaipan

命令行格式
==========

Usage::
    
    Usage: netdisk [options] command [argument ...]
    
    Commands: info,put,mv,ls,get,ask,rm,cp,cat
    
    Options:
      --version     show program's version number and exit
      -h, --help    show this help message and exit
      -q, --quiet   don't print status messages to stdout
      -n NETDISK    netdisk type: dropbox, kuaipan
      -a APPTOKEN   netdisk app token
      -u USERTOKEN  user access token
      -d DESTTOKEN  destination user access token, for copy between two users

Sample::

    # 申请一个新的用户token
    netdisk -a apptoken ask
    # 查看目录
    netdisk -a apptoken -u usertoken ls

API 
=====
1. `Dropbox API <https://www.dropbox.com/developers>`_
2. `Kuapan API <http://www.kuaipan.cn/developers/document.htm>`_

