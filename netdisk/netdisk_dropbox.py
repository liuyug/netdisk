import sys
import locale
import os

from netdisk.dropbox import client, session

from netdisk.base import exectime, command, sizeof_fmt, NetworkDisk, FileCallback, file_callback

ACCESS_TYPE = 'app_folder'  # should be 'dropbox' or 'app_folder' as configured for your app


class Dropbox(NetworkDisk):
    version = '1.5.1'

    def __init__(self, apptoken, usertoken=None):
        super(Dropbox, self).__init__(apptoken, usertoken)
        if apptoken:
            self.session = session.DropboxSession(*apptoken.split('|'), access_type=ACCESS_TYPE)
        if usertoken:
            self.session.set_token(*usertoken.split('|'))
            self.api_client = client.DropboxClient(self.session)

    def to_token(self, key, secret):
        return session.OauthToken(key, secret)

    def ask_token_url(self, callback=None):
        request_token = self.session.obtain_request_token()
        url = self.session.build_authorize_url(request_token, oauth_callback=callback)
        return request_token, url

    def obtain_access_token(self, request_token):
        self.session.obtain_access_token(request_token)
        token = '%s|%s'% (self.session.token.key, self.session.token.secret)
        return token

    @command(login_required=False)
    def is_login(self):
        return self.session.is_linked()

    @exectime
    @command()
    def put(self, from_path, to_path):
        from_file = FileCallback(os.path.expanduser(from_path),
                "rb", callback=file_callback)
        print('Uploading %s => %s' % (from_path, to_path))
        ret = self.api_client.put_file(to_path, from_file)
        sys.stdout.write('\n')  # to keep process bar
        return ret.get('bytes', 0)

    @exectime
    @command()
    def get(self, from_path, to_path=''):
        if not to_path:
            to_path = os.path.basename(from_path)
        to_file = open(os.path.expanduser(to_path), "wb")
        f, metadata = self.api_client.get_file_and_metadata(from_path)
        print('Downloading %s => %s: %s' %
                (from_path, to_path, metadata['size'].encode('utf-8')))
        total_size = metadata.get('bytes', 0)
        cur_size = 0
        bufsize = 4096
        data = f.read(bufsize)
        while data != '':
            cur_size += len(data)
            to_file.write(data)
            file_callback(cur_size, total_size)
            data = f.read(bufsize)
        sys.stdout.write('\n')  # to keep process bar
        to_file.close()
        return total_size

    @exectime
    @command()
    def ls(self, path='/'):
        resp = self.api_client.metadata(path)

        if 'contents' in resp:
            for f in resp['contents']:
                size = ''
                folder=''
                if f['is_dir']:
                    folder='/'
                else:
                    #size = f['bytes']
                    size = f['size']
                name = f['path']
                encoding = locale.getdefaultlocale()[1]
                sys.stdout.write(('%9s %s%s\n' % (size,name,folder)).encode(encoding))

    @exectime
    @command()
    def rm(self, path):
        """delete a file or directory"""
        self.api_client.file_delete(path)

    @exectime
    @command()
    def cat(self, path):
        """cat a file"""
        f, metadata = self.api_client.get_file_and_metadata(path)
        sys.stdout.write(f.read())

    @exectime
    @command()
    def cp(self, netdisk, from_path, to_path):
        """copy file to another user"""
        copy_ref = self.api_client.create_copy_ref(from_path)['copy_ref']
        metadata = netdisk.api_client.add_copy_ref(copy_ref, to_path)
        return metadata

    @exectime
    @command()
    def mv(self, from_path, to_path):
        """move/rename a file or directory"""
        self.api_client.file_move(from_path, to_path)

    @command()
    def account_info(self):
        """display account information"""
        def output(metadata, prefix=''):
            for k, v in metadata:
                if k == 'quota_info':
                    print('%squota info:' % prefix)
                    output(sorted(v.items()), prefix=' ' * 4)
                    continue
                elif k in ['normal', 'quota']:
                    v = sizeof_fmt(v)
                print('%s%s => %s' % (prefix, k, v))

        f = self.api_client.account_info()
        output(sorted(f.items()))
