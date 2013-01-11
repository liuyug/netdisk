#/bin/env python

def command(login_required=True):
    """a decorator for handling authentication and exceptions"""
    def decorate(f):
        def wrapper(self, args):
            if login_required and not self.is_login():
                sys.stdout.write("Please 'login' to execute this command\n")
                return

            try:
                return f(self, *args)
            except Exception, e:
                sys.stdout.write(str(e) + '\n')

        wrapper.__doc__ = f.__doc__
        return wrapper
    return decorate

class NetworkDisk(object):
    def __init__(self, token=None):
        self.session = None
        self.api_client = None

    def ask_token(self, *args):
        raise NotImeplement

    def is_login(self):
        return False

    @command()
    def put(self, from_path, to_path, *args):
        raise NotImeplement

    @command()
    def get(self, from_path, to_path, *args):
        raise NotImeplement

    @command()
    def ls(self, path='', *args):
        raise NotImeplement

    @command()
    def rm(self, path, *args):
        raise NotImeplement

    @command()
    def mv(self, from_path, to_path, *args):
        raise NotImeplement

    @command()
    def account_info(self, *args):
        raise NotImeplement

