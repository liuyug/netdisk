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
        'cat':'cat',
        'mv':'mv',
        'cp':'cp',
        'info':'account_info'}
Netdisk = {'dropbox':Dropbox,
        }
def main():
    usage = "usage: %prog [options] command [argument ...]"
    desc = "Commands: %s"% ','.join(Commands.keys())
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
    parser.add_option("-d", "",
            action="store", dest="desttoken", default='',
            help="destination user access token, for copy between two users")
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
    if args[0] == 'cp':
        if options.desttoken:
            net_disk2 = Netdisk[options.netdisk](options.apptoken, options.desttoken)
        else:
            net_disk2 = net_disk
        if not net_disk2.is_login():
            net_disk2.ask_token()
        net_disk.cp(net_disk2, *args[1:])
        sys.exit(0)
    cmd = getattr(net_disk, Commands[args[0]])
    cmd(*args[1:])

if __name__ == '__main__':
    main()

