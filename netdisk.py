#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
try:
    from configparser import ConfigParser
except:
    from ConfigParser import ConfigParser

from netdisk import Dropbox
from netdisk import Kuaipan
from netdisk import __version__

Commands = {
    'ask':   'ask_token',
    'put':   'put',
    'get':   'get',
    'ls':    'ls',
    'rm':    'rm',
    'cat':   'cat',
    'mv':    'mv',
    'cp':    'cp',
    'info':  'account_info'
}

Netdisk = {
    'dropbox': Dropbox,
    'kuaipan': Kuaipan,
}


def saveConfig(config_file, diskname, netdisk, apptoken, usertoken):
    config = ConfigParser()
    config.add_section(diskname)
    config.set(diskname, 'netdisk', netdisk)
    config.set(diskname, 'apptoken', apptoken)
    config.set(diskname, 'usertoken', usertoken)
    with open(config_file, 'w') as f:
        config.write(f)


def loadConfig(config_file, diskname):
    disk = {}
    if diskname:
        config = ConfigParser()
        config.read(config_file)
        if diskname in config.sections():
            disk['netdisk'] = config.get(diskname, 'netdisk')
            disk['apptoken'] = config.get(diskname, 'apptoken')
            disk['usertoken'] = config.get(diskname, 'usertoken')
    return disk


def main():
    config_dir = os.path.join(os.path.expanduser('~'), '.config', 'netdisk')
    config_file = os.path.join(config_dir, 'netdisk.conf')
    if not os.path.exists(config_dir):
        os.mkdir(config_dir)

    ver = '''%%(prog)s %s\n\nModule:\n%s''' % (
        __version__,
        '\n'.join(['    %s: %s' % (x, xc.version) for x, xc in Netdisk.items()])
    )
    parser = argparse.ArgumentParser(
        description='Module:\n%s' %
        '\n'.join(['    %s: %s' % (x, xc.version) for x, xc in Netdisk.items()]),
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--version', action='version', version=ver)
    parser.add_argument('-v', '--verbose', help='verbose help',
                        action='count', default=0)
    parser.add_argument('--d1', dest='diskname1', help='netdisk name in config')
    parser.add_argument('--d2', dest='diskname2',
                        help='netdisk name in config, the destination in command cp')
    parser.add_argument('-n', dest='netdisk', metavar='TYPE', choices=Netdisk.keys(),
                        help="netdisk type: %s" % ', '.join(Netdisk.keys()))
    parser.add_argument('-a', dest='apptoken', help='netdisk app token')
    parser.add_argument('-u', dest='usertoken', help='user access token')
    parser.add_argument('-d', dest='desttoken',
                        help='destination user access token, for copy between two users')
    parser.add_argument('command', metavar='command', choices=Commands.keys(),
                        help='Support: %s' % ', '.join(Commands.keys()))
    parser.add_argument('paths', metavar='path', nargs='*', help='directory or files')
    args = parser.parse_args()

    disk = loadConfig(config_file, args.diskname1)
    netdisk = args.netdisk if args.netdisk else disk.get('netdisk')
    apptoken = args.apptoken if args.apptoken else disk.get('apptoken')
    usertoken = args.usertoken if args.usertoken else disk.get('usertoken')
    disk2 = loadConfig(config_file, args.diskname2)
    desttoken = args.desttoken if args.desttoken else disk2.get('usertoken')

    net_disk = Netdisk[netdisk](apptoken, usertoken)
    if args.command == 'ask':
        token = net_disk.ask_token()
        if args.diskname1:
            saveConfig(config_file, args.diskname1, netdisk, apptoken, token)
        return
    if not net_disk.is_login():
        token = net_disk.ask_token()
        if args.diskname1:
            saveConfig(config_file, args.diskname1, netdisk, apptoken, token)
    if args.command == 'cp':
        if desttoken:
            net_disk2 = Netdisk[netdisk](apptoken, desttoken)
        else:
            net_disk2 = net_disk
        if not net_disk2.is_login():
            token = net_disk2.ask_token()
            if args.diskname2:
                saveConfig(config_file, args.diskname2, netdisk, apptoken, token)
        net_disk.cp(net_disk2, *args.paths)
        return
    cmd = getattr(net_disk, Commands[args.command])
    cmd(*args.paths)

if __name__ == '__main__':
    main()
