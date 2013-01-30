
import sys
import time

def exectime(func):
    def newFunc(self, *args):
        t0 = time.time()
        ret = func(self, *args)
        t1 = time.time()
        print '-'*80
        print 'Spend %.3fs on function, %s'% (t1-t0, func.__name__)
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
                sys.stdout.write(str(e) + '\n')

        wrapper.__doc__ = f.__doc__
        wrapper.__name__ = f.__name__
        return wrapper
    return decorate

class NetworkDisk(object):
    def __init__(self, token, usertoken):
        self.session = None
        self.api_client = None

    @command(login_required=False)
    def ask_token(self):
        raise NotImeplement

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

