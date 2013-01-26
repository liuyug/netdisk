#coding:utf-8
#author: leanse

"""
"""

import oauth.oauth as oauth
from http_client import http_client
from urllib import quote

def to_str(x):
    _to_str = lambda i: x if not isinstance(x, unicode) else x.encode("utf-8")
    if not isinstance(x, (str, unicode)):
        return str(x)
    return _to_str(x)

class KuaipanSession():
    API_VERSION = 1
    API_HOST = "openapi.kuaipan.cn"
    CONTENT_HOST = "api-content.dfs.kuaipan.cn"
    CONV_HOST = "conv.kuaipan.cn"
    AUTH_HOST = "https://www.kuaipan.cn/api.php?ac=open&op=authorise&oauth_token="

    def __init__(self, consumer_key, consumer_secret, access_type):
        assert access_type in ['kuaipan', 'app_folder']
        self.consumer = oauth.OAuthConsumer(consumer_key, consumer_secret)
        self.signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()
        self.root = access_type
        self.request_token = None
        self.token = None

    def request(self, url, token, params, http_method):
        request = oauth.OAuthRequest.from_consumer_and_token(self.consumer, token = token,
                    http_method = http_method, http_url = url, parameters = params)
        request.sign_request(self.signature_method, self.consumer, token)
        return request.to_url()
        
    def set_request_token(self, request_token, request_token_secret):
        self.request_token = oauth.OAuthToken(request_token, request_token_secret)

    def set_access_token(self, access_token, access_token_secret):
        self.token = oauth.OAuthToken(access_token, access_token_secret)

    def is_linked(self):
        return bool(self.token)

    def unlink(self):
        self.token = None  

    def obtain_request_token(self, callback = None):
        self.unlink() 
        url = self.build_authorize_url(self.API_HOST, "/open/requestToken", callback = callback)
        ret = http_client.GET(url)
        self.request_token = oauth.OAuthToken(ret['oauth_token'], ret['oauth_token_secret'])
        return self.request_token

    def obtain_access_token(self, request_token = None):
        self.unlink()
        request_token = request_token or self.request_token
        assert request_token
        url = self.build_url(self.API_HOST, "/open/accessToken", token = request_token, security = True)
        ret = http_client.GET(url)
        self.token = oauth.OAuthToken(ret['oauth_token'], ret['oauth_token_secret'])
        return self.token

    def build_url(self, host, target, token = None, params = None, http_method = 'GET', security = False):
        url = self.build_path(host, target, security)
        token = token if token else self.token
        return self.request(url, token,  params, http_method)

    def build_authorize_url(self, host, target, token = None, callback = None):
        params = {}
        if callback:
            params['oauth_callback'] = callback
        params = None if not params else params
        return self.build_url(host, target, token, params, security = True)

    def build_path(self, host, target, security):
        target = to_str(target)
        target_path = quote(target)
        if not host.startswith(("http://", "https://")):
            schema = "https://" if security else "http://"
        else:
            schema = ""
        return schema + host + target_path
        


if __name__ == "__main__":
    pass
