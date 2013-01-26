#coding:utf-8
#author: leanse

import urllib2
import cookielib
import socket
import json

class SocketErr(socket.error):
    def __init__(self, host, e):
        msg = "Error connecting to \"%s\": %s" % (host, str(e))
        socket.error.__init__(self, msg)

class ErrorRespon(Exception):
    def __init__(self, code, reason, body = None):
        self.code = code
        self.reason = reason
        self.body = body

    def __str__(self):
        return "HTTPCode = %d, reason = %s, body = %s" % (
            int(self.code), self.reason, self.body)

def to_str(s):
    _to_str = lambda x: x.encode("utf-8") if isinstance(x, unicode) else x
    if not isinstance(s, (str, unicode)):
        return str(s)
    return _to_str(s)

class http_client(object):
    @staticmethod
    def request(url, postdata = None, header = {}):
        req = urllib2.Request(url, postdata, header)
        try:
            res = urllib2.urlopen(req)
            return res.read()
        except urllib2.HTTPError, e:
            if hasattr(e, 'code'):
                raise ErrorRespon(e.code, e.read())
            raise SocketErr(url, e)

    @staticmethod
    def handleResult(ret):
        return json.loads(ret)
    
    @classmethod
    def GET(cls, url, header = {}):
        ret = cls.request(url, header = header)
        return cls.handleResult(ret)

    @classmethod
    def POST(cls, url, post = None, header = {}):
        ret = cls.request(url, post, header)
        return cls.handleResult(ret)

    @classmethod
    def MultiPartPost(cls, url, data, file_name):
        from poster.encode import multipart_encode
        from poster.encode import MultipartParam
        from poster.streaminghttp import register_openers
        
        register_openers()
        if hasattr(data, 'read'):
            p = MultipartParam("file", fileobj = data, filename = file_name)
        else:
            p = MultipartParam("file", value = data, filename = file_name)
        datagen, headers = multipart_encode([p])
        return cls.request(url, datagen, headers) 

    @staticmethod
    def DownloadFile(url):
        cookie_handler = urllib2.HTTPCookieProcessor(cookielib.CookieJar())
        redire_handler = urllib2.HTTPRedirectHandler()
        opener = urllib2.build_opener(cookie_handler, redire_handler)
        urllib2.install_opener(opener)
        
        req = urllib2.Request(url)
        try:
            res = urllib2.urlopen(req)
            return res
        except urllib2.HTTPError, e:
            if hasattr(e, 'code'):
                raise ErrorRespon(e.code, e.read())
            raise SocketErr(url, e)
        
    @staticmethod
    def ConverFile(url):
        cookie_handler = urllib2.HTTPCookieProcessor(cookielib.CookieJar())
        redire_handler = urllib2.HTTPRedirectHandler()
        opener = urllib2.build_opener(cookie_handler, redire_handler)
        urllib2.install_opener(opener)

        req = urllib2.Request(url)
        try:
            res = urllib2.urlopen(req)
            return res.read()
        except urllib2.HTTPError, e:
            if hasattr(e, 'code'):
                raise ErrorRespon(e.code, e.read())
            raise SocketErr(url, e)

