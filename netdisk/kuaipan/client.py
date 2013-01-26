#coding:utf-8
#author: leanse

"""
"""

import re
from http_client import http_client
from session import KuaipanSession
from session import to_str

def format_path(path):
    if not path:
        return path

    path = re.sub(r'/+', '/', path)
    if path == '/':
        return ""
    else:
        return '/' + path.strip('/') 

class KuaipanAPI():
    def __init__(self, session):
        self.session = session
        self.host = None
    
    def request(self, target, params = None, method = 'GET', server = 'API'):
        assert method in ['GET', 'POST']
        host = {'API': self.session.API_HOST, 'CONTENT': self.session.CONTENT_HOST,
                'CONV': self.session.CONV_HOST}
        url = self.session.build_url(host[server], target, params = params, http_method = method)
        if method == 'GET':
            return http_client.GET(url)
        return url
    
    def requestToken(self, callback = None):
        token = self.session.obtain_request_token(callback)
        return self.session.AUTH_HOST + token.key

    def accessToken(self):
        access_token = self.session.obtain_access_token()
        return access_token

    def account_info(self):
        return self.request("/1/account_info")

    def metadata(self, path, list = True):
        target = "/1/metadata/%s%s" % (self.session.root, format_path(path))
        params = dict(list = ("true" if list else "false"))
        return self.request(target, params)

    def shares(self, path):
        target = "/1/shares/%s%s" % (self.session.root, format_path(path))
        return self.request(target)

    def create_folder(self, path):
        params = dict(root = self.session.root, path = to_str(path))
        return self.request("/1/fileops/create_folder", params)

    def delete(self, path):
        params = dict(root = self.session.root, path = to_str(path))
        return self.request("/1/fileops/delete", params)

    def move(self, from_path, to_path):
        params = dict(root = self.session.root, from_path = to_str(from_path), to_path = to_str(to_path))
        return self.request("/1/fileops/move", params)

    def copy(self, from_path, to_path):
        params = dict(root = self.session.root, from_path = to_str(from_path), to_path = to_str(to_path))
        return self.request("/1/fileops/copy", params)

    def add_copy_ref(self, from_copy_ref, to_path):
        params = dict(root = self.session.root, from_copy_ref = to_str(from_copy_ref), to_path = to_str(to_path))
        return self.request("/1/fileops/copy", params)

    def create_copy_ref(self, path):
        target = "/1/copy_ref/%s%s" % (self.session.root, format_path(path))
        return self.request(target)

    def get_upload_locate(self):
        ret = self.request("/1/fileops/upload_locate", server = 'CONTENT')
        return ret['url']

    def upload_file(self, path, data, overwrite):
        if not self.host:
            self.host = self.get_upload_locate()
        overwrite = "True" if overwrite else "False"
        params = dict(root = self.session.root, path = to_str(path), overwrite = overwrite)
        url = self.session.build_url(self.host, "1/fileops/upload_file", params = params, http_method = "POST")
        ret = http_client.MultiPartPost(url, data, "kfile")
        return ret

    def download_file(self, path):
        params = dict(root = self.session.root, path = to_str(path))
        url = self.session.build_url(self.session.CONTENT_HOST, "/1/fileops/download_file", params = params)
        return http_client.DownloadFile(url)

    def thumbnail(self, path, width, height):
        params = dict(root = self.session.root, path = to_str(path), width = to_str(width), height = to_str(height))
        url = self.session.build_url(self.session.CONV_HOST, "/1/fileops/thumbnail", params = params)
        ret = http_client.ConverFile(url)
        return ret

    def document_view(self, path, view, type, zip = 0):
        params = dict(root = self.session.root, path = to_str(path), view = view, type = type, zip = to_str(zip))
        url = self.session.build_url(self.session.CONV_HOST, "/1/fileops/documentView", params = params)
        ret = http_client.ConverFile(url)
        return ret
