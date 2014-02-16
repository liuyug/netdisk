import sys
import os
import locale
import json

from netdisk.kuaipan import client, session

from netdisk.base import exectime, command, NetworkDisk, sizeof_fmt, FileCallback, file_callback

ACCESS_TYPE = 'app_folder'  # should be 'dropbox' or 'app_folder' as configured for your app


class Kuaipan(NetworkDisk):
    version = '0.1beta'

    def __init__(self, apptoken, usertoken=None):
        super(Kuaipan, self).__init__(apptoken, usertoken)
        if apptoken:
            self.session = session.KuaipanSession(*apptoken.split('|'), access_type=ACCESS_TYPE)
        if usertoken:
            self.session.set_access_token(*usertoken.split('|'))
            self.api_client = client.KuaipanAPI(self.session)

    def to_token(self, key, secret):
        return session.oauth.OAuthToken(key, secret)

    def ask_token_url(self, callback=None):
        request_token = self.session.obtain_request_token()
        url = '%s%s'% (self.session.AUTH_HOST, request_token.key)
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
        path = os.path.dirname(to_path)
        if path:
            self.api_client.create_folder(path)
        print('Uploading %s => %s' % (from_path, to_path))
        ret = self.api_client.upload_file(to_path, from_file, False)
        sys.stdout.write('\n')  # to keep process bar
        ret = json.loads(ret)
        return int(ret.get('size', '0'))

    @exectime
    @command()
    def get(self, from_path, to_path=''):
        if not to_path:
            to_path = os.path.basename(from_path)
        to_file = FileCallback(os.path.expanduser(to_path), "wb")
        rs = self.api_client.download_file(from_path)
        md = self.api_client.metadata(from_path)
        total_size = md.get('size', 0)
        cur_size = 0
        bufsize = 4096
        print('Downloading %s => %s: %s' %
                (from_path, to_path, sizeof_fmt(total_size)))
        data = rs.read(bufsize)
        while data != '':
            cur_size += len(data)
            to_file.write(data)
            file_callback(cur_size, total_size)
            data = rs.read(bufsize)
        sys.stdout.write('\n')  # to keep process bar
        to_file.close()
        return total_size

    @exectime
    @command()
    def ls(self, path='/'):
        path = os.path.join('/', path)
        resp = self.api_client.metadata(path)
        if 'files' in resp:
            for f in resp['files']:
                size = ''
                folder=''
                if f['type'] == 'folder':
                    folder='/'
                else:
                    size = f['size']
                    size = sizeof_fmt(size)
                name = os.path.join(path,f['name'])
                encoding = locale.getdefaultlocale()[1]
                sys.stdout.write(('%9s %s%s\n' % (size,name,folder)).encode(encoding))

    @exectime
    @command()
    def rm(self, path):
        """delete a file or directory"""
        self.api_client.delete(path)

    @exectime
    @command()
    def cat(self, path):
        """cat a file"""
        rs=self.api_client.download_file(path)
        sys.stdout.write(rs.read())

    @exectime
    @command()
    def cp(self, netdisk, from_path, to_path):
        """copy file to another user"""
        copy_ref = self.api_client.create_copy_ref(from_path)['copy_ref']
        rs = netdisk.api_client.add_copy_ref(copy_ref, to_path)
        return rs

    @exectime
    @command()
    def mv(self, from_path, to_path):
        """move/rename a file or directory"""
        path=os.path.dirname(to_path)
        if path:
            self.api_client.create_folder(path)
        self.api_client.move(from_path, to_path)

    @command()
    def account_info(self):
        """display account information"""
        f = self.api_client.account_info()
        for k, v in sorted(f.items()):
            if k in ['max_file_size', 'quota_total', 'quota_used']:
                v = sizeof_fmt(v)
            print('%s => %s' % (k, v))
