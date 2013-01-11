#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from optparse import OptionParser

from netdisk_dropbox import Dropbox

Commands = {'ask':'ask_token',
        'put':'put',
        'get':'get',
        'ls':'ls',
        'rm':'rm',
        'mv':'mv',
        'info':'account_info'}
Netdisk = {'dropbox':Dropbox,
        }
def main():
    usage = "usage: %prog [options] command [argument ...]"
    desc = "Commands: ask, put, get, ls, rm, mv, info"
    sample = "Sample: netdisk_cli.py -a apptoken -u usertoken ls"
    parser = OptionParser(usage, description=desc, epilog=sample)
    parser.add_option("-q", "--quiet",
            action="store_false", dest="verbose", default=True,
            help="don't print status messages to stdout")
    parser.add_option("-n", "",
            action="store", dest="netdisk", default='dropbox',
            help="netdisk type: dropbox")
    parser.add_option("-a", "",
            action="store", dest="apptoken", default='',
            help="netdisk app token")
    parser.add_option("-u", "",
            action="store", dest="usertoken", default='',
            help="user access token")
    (options, args) = parser.parse_args()
    if not args: 
        parser.print_help()
        sys.exit(1)
    if args[0] not in Commands:
        print('command error!')
        sys.exit(1)
    net_disk = Netdisk[options.netdisk](options.apptoken, options.usertoken)
    if args[0] == 'ask':
        net_disk.ask_token()
        sys.exit(0)
    if not net_disk.is_login():
        net_disk.ask_token()
    cmd = getattr(net_disk, Commands[args[0]])
    cmd(args[1:])

if __name__ == '__main__':
    main()

