#/bin/env python
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
    parser = OptionParser(usage)
    parser.add_option("-n", "--netdisk",
            action="store", dest="netdisk", default='dropbox',
            help="netdisk type: dropbox")
    parser.add_option("-t", "--token",
            action="store", dest="token", default='',
            help="user access token")
    parser.add_option("-q", "--quiet",
            action="store_false", dest="verbose", default=True,
            help="don't print status messages to stdout")
    (options, args) = parser.parse_args()
    if not args: 
        parser.print_help()
        sys.exit(1)
    if args[0] not in Commands:
        print('command error!')
        sys.exit(1)
    net_disk = Netdisk[options.netdisk](options.token)
    if args[0] == 'ask':
        net_disk.ask_token()
        sys.exit(0)
    if not net_disk.is_login():
        net_disk.ask_token()
    cmd = getattr(net_disk, Commands[args[0]])
    cmd(args[1:])

if __name__ == '__main__':
    main()
    user_token = '4g072xbgw1wj5uy|x7w4mjf2nlbrrtm'

