# -*- coding:utf-8 -*-
from baidumap.core.controller import Controller
from baidumap.util.url import Url
from baidumap.config import base_url
from baidumap.object import BaiduMapObject
from baidumap.api.exceptions import HandleNotExistsError

from urllib.parse import urljoin


class Handle:
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
        return

    def set_params(self, **kwargs):
        '''
        use format as "key=value", can set any number of param in one time
        '''
        self._url.add_map(kwargs)

    def set_name(self, name):
        self._url = Url(urljoin(base_url, name))

    def run(self, collect_keys=None, **kwargs):
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
