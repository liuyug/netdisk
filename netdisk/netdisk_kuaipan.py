import sys
import os
import locale
import pprint

from kuaipan import client, session

from base import exectime, command, NetworkDisk

ACCESS_TYPE = 'app_folder'  # should be 'dropbox' or 'app_folder' as configured for your app

class Kuaipan(NetworkDisk):
    version = '0.1beta'
    def __init__(self, apptoken, usertoken):
        super(Kuaipan, self).__init__(apptoken,usertoken)
        if apptoken:
            self.session = session.KuaipanSession(*apptoken.split('|'), access_type=ACCESS_TYPE)
        if usertoken:
            self.session.set_access_token(*usertoken.split('|'))
            self.api_client = client.KuaipanAPI(self.session)

    @command(login_required=False)
    def ask_token(self):
        request_token = self.session.obtain_request_token()
        url = '%s%s'% (self.session.AUTH_HOST, request_token.key)
        print "url:", url
        print "Please authorize in the browser. After you're done, press enter."
        raw_input()
        self.session.obtain_access_token(request_token)
        print('token: %s|%s'%(self.session.token.key, self.session.token.secret))

    @command(login_required=False)
    def is_login(self):
        return self.session.is_linked() 

    @exectime
    @command()
    def put(self, from_path, to_path):
        from_file = open(os.path.expanduser(from_path), "rb")
        path=os.path.dirname(to_path)
        if path:
            self.api_client.create_folder(path)
        ret=self.api_client.upload_file(to_path, from_file, False)

    @exectime
    @command()
    def get(self, from_path, to_path):
        to_file = open(os.path.expanduser(to_path), "wb")
        rs=self.api_client.download_file(to_path)
        to_file.write(rs.read())

    @exectime
    @command()
    def ls(self, path=''):
        resp = self.api_client.metadata(path)
        if 'files' in resp:
            for f in resp['files']:
                name = os.path.basename(f['name'])
                encoding = locale.getdefaultlocale()[1]
                sys.stdout.write(('%s\n' % name).encode(encoding))

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
        pprint.PrettyPrinter(indent=2).pprint(f)

