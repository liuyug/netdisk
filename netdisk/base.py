
import os
import sys
import time


def sizeof_fmt(num):
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0 and num > -1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0
    return "%3.1f %s" % (num, 'TB')


class NotImeplement(Exception):
    pass


def exectime(func):
    def newFunc(self, *args):
        t0 = time.time()
        ret = func(self, *args)
        t1 = time.time()
        print('-' * 80)
        if ret and func.__name__ in ['get', 'put']:
            print('Spend %.3fs(%s/s) on "%s"' %
                    (t1 - t0, sizeof_fmt(ret / (t1 - t0)), func.__name__))
        else:
            print('Spend %.3fs on "%s"' % (t1 - t0, func.__name__))
        return ret
    return newFunc


def command(login_required=True):
    """a decorator for handling authentication and exceptions"""
    def decorate(f):
        def wrapper(self, *args):
            if login_required and not self.is_login():
                sys.stdout.write("Please 'login' to execute this command\n")
                return

            try:
                return f(self, *args)
            except Exception, e:
                sys.stdout.write('%s: %s\n' % (f.__name__, str(e)))

        wrapper.__doc__ = f.__doc__
        wrapper.__name__ = f.__name__
        return wrapper
    return decorate


class NetworkDisk(object):
    def __init__(self, token, usertoken=None):
        self.session = None
        self.api_client = None

    def to_token(self, key, secret):
        raise NotImeplement

    def ask_token_url(self, callback=None):
        request_token = ''
        url = ''
        return request_token, url

    def obtain_access_token(self, request_token):
        token = ''
        return token

    @command(login_required=False)
    def ask_token(self):
        request_token, url = self.ask_token_url()
        print "url:", url
        print "Please authorize in the browser. After you're done, press enter."
        raw_input()
        token = self.obtain_access_token(request_token)
        print('token: %s' % token)
        return token

    @command(login_required=False)
    def is_login(self):
        return False

    @command()
    def put(self, from_path, to_path):
        raise NotImeplement

    @command()
    def get(self, from_path, to_path):
        raise NotImeplement

    @command()
    def ls(self, path=''):
        raise NotImeplement

    @command()
    def rm(self, path):
        raise NotImeplement

    @command()
    def cat(self, path):
        raise NotImeplement

    @command()
    def cp(self, client, from_path, to_path):
        raise NotImeplement

    @command()
    def mv(self, from_path, to_path):
        raise NotImeplement

    @command()
    def account_info(self):
        raise NotImeplement


def file_callback(num, total):
    percent = num * 100.0 / total
    bar = int(percent / 2)
    sys.stdout.write('[%s%s%s] %.2f %%\r' % (
        '=' * bar,
        '>' if bar < 50 else '=',
        ' ' * (50 - bar),
        percent))
    sys.stdout.flush()


class FileCallback(file):
    def __init__(self, filename, mode='r', bufsize=-1, callback=file_callback):
        super(FileCallback, self).__init__(filename, mode, bufsize)
        super(FileCallback, self).seek(0, os.SEEK_END)
        self.length = self.tell()
        super(FileCallback, self).seek(0, os.SEEK_SET)
        self.callback = callback
        self.cur_pos = 0

    def read(self, size):
        data = super(FileCallback, self).read(size)
        self.cur_pos += len(data)
        self.callback(self.cur_pos, self.length)
        return data

    def seek(self, offset, where=os.SEEK_SET):
        super(FileCallback, self).seek(offset, where)
        self.cur_pos = self.tell()
        self.callback(self.cur_pos, self.length)
