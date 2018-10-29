# -*- coding:utf-8 -*-
from urllib.parse import urljoin

from baidumap.core.controller import Controller
from baidumap.core.static import base_url
from baidumap.object import BaiduMapObject
from baidumap.util import log
from baidumap.util.url import Url


class Handle(object):
    '''
    handle of baidu map api
    '''

    def __init__(self, ak_key, url='', is_list=False, **kwargs):
        '''
        use format as "key=value", can set any number of param in one time
        '''
        self._controller = Controller(ak_key)
        self._url = Url(url)
        self._url.add_map(kwargs)
        self.is_list = is_list
        log.debug('handle created, name: %s' % self.get_name())
        return

    def set_params(self, **kwargs):
        '''
        use format as "key=value", can set any number of param in one time
        '''
        self._url.add_map(kwargs)

    def set_name(self, name):
        self._url = Url(urljoin(base_url, name))

    def get_name(self):
        base_length = len(base_url)
        raw_url = self._url._raw_url
        if len(raw_url) > base_length:
            return raw_url[base_length:]
        else:
            return 'raw_handle'

    def run(self, collect_keys=None, **kwargs):
        log.info('%s is running' % (self.get_name()))
        result = dict()
        if self.is_list:
            # default collect all
            result = self._controller.get_list(self._url, collect_keys,
                                               **kwargs)
        else:
            # default collect all
            result = self._controller.get_single(self._url, collect_keys,
                                                 **kwargs)

        return BaiduMapObject(result)

    pass


def get_handle(ak_key, name='', is_list=False, **kwargs):
    handle_raw_url = urljoin(base_url, name)
    return Handle(ak_key, handle_raw_url, is_list, **kwargs)
