# -*- coding: utf-8 -*-

from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware


class ProxyMiddleware(HttpProxyMiddleware):

    def __init__(self, proxies):
        self.proxies = proxies

    def process_request(self, request, spider):
        request.meta['proxy'] = self.proxy_shadowsocks()

    @staticmethod
    def proxy_xxnet():
        proxy = "http://127.0.0.1:8087"
        return proxy

    @staticmethod
    def proxy_shadowsocks():
        proxy = "http://127.0.0.1:1080"
        return proxy
