import sys
import locale
import os
import pprint
import shlex
from optparse import OptionParser

from dropbox import client, rest, session

from base import command, NetworkDisk

ACCESS_TYPE = 'app_folder'  # should be 'dropbox' or 'app_folder' as configured for your app

class Dropbox(NetworkDisk):
    version = '1.5.1'
    def __init__(self, apptoken, usertoken):
        super(Dropbox, self).__init__(apptoken,usertoken)
        if apptoken:
            self.session = session.DropboxSession(*apptoken.split('|'), access_type=ACCESS_TYPE)
        if usertoken:
            self.session.set_token(*usertoken.split('|'))
            self.api_client = client.DropboxClient(self.session)

    def ask_token(self):
        request_token = self.session.obtain_request_token()
        url = self.session.build_authorize_url(request_token)
        print "url:", url
        print "Please authorize in the browser. After you're done, press enter."
        raw_input()
        self.session.obtain_access_token(request_token)
        print('token: %s|%s'%(self.session.token.key, self.session.token.secret))

    def is_login(self):
        return self.session.is_linked() 

    @command()
    def put(self, from_path, to_path):
        from_file = open(os.path.expanduser(from_path), "rb")
        self.api_client.put_file(to_path, from_file)

    @command()
    def get(self, from_path, to_path):
        to_file = open(os.path.expanduser(to_path), "wb")

        f, metadata = self.api_client.get_file_and_metadata(from_path)
        print 'Metadata:', metadata
        to_file.write(f.read())

    @command()
    def ls(self, path=''):
        resp = self.api_client.metadata(path)

        if 'contents' in resp:
            for f in resp['contents']:
                name = os.path.basename(f['path'])
                encoding = locale.getdefaultlocale()[1]
                sys.stdout.write(('%s\n' % name).encode(encoding))

    @command()
    def rm(self, path):
        """delete a file or directory"""
        self.api_client.file_delete(path)

    @command()
    def cat(self, path):
        """cat a file"""
        f, metadata = self.api_client.get_file_and_metadata(path)
        sys.stdout.write(f.read())

    @command()
    def cp(self, netdisk, from_path, to_path):
        copy_ref = self.api_client.create_copy_ref(from_path)['copy_ref']
        metadata = netdisk.api_client.add_copy_ref(copy_ref, to_path)

    @command()
    def mv(self, from_path, to_path):
        """move/rename a file or directory"""
        self.api_client.file_move(from_path, to_path)

    @command()
    def account_info(self):
        """display account information"""
        f = self.api_client.account_info()
        pprint.PrettyPrinter(indent=2).pprint(f)

