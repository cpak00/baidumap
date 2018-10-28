# -*- coding:utf-8 -*-
from baidumap.core.collector import Collector
from baidumap.api.exceptions import get_exception, NetError

from requests.exceptions import RequestException


class Controller:
    '''
    baidu api core controller
    '''

    def __init__(self, ak_key):
        self._collector = Collector(ak_key)
        return

    def get_single(self, url, collect_keys=None):
        '''
        return single result
        '''
        try:
            status, single_result = self._collector.get_single_result(
                url, collect_keys=collect_keys)
            if not status.is_ok():
                raise get_exception(status)
            else:
                return single_result
        except RequestException as e:
            raise NetError() from e

    def get_list(self, url, collect_keys=None, **kwargs):
        '''
        return list result
        '''
        try:
            status, list_result = self._collector.get_list_result(
                url, collect_keys=collect_keys, **kwargs)
            if not status.is_ok():
                raise get_exception(status)
            else:
                return list_result
        except RequestException as e:
            raise NetError() from e

    pass
