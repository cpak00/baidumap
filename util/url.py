# -*- coding:utf-8 -*-
import requests


class Url:
    '''
    Url for api request
    '''
    def __init__(self, p_raw_url):
        '''
        Url()->None: init a Url object
        '''
        self._raw_url = p_raw_url
        self._params = dict()
        return

    def __str__(self):
        return '%s?%s' % (self._raw_url, '&'.join(self._params))

    def get(self):
        '''
        get()->Response<>
        '''
        r = requests.get(self._raw_url, params=self._params)
        r.encoding = 'utf-8'
        return r

    def set_raw_url(self, p_raw_url):
        '''
        set_raw_url(p_raw_url: str)->None: set the raw url
        '''
        self._raw_url = p_raw_url
        return

    def set_param(self, p_key, p_value):
        '''
        set_param(p_key, p_value)->None: add a request param
        '''
        self._params[p_key] = p_value
        return

    def add_map(self, p_map):
        '''
        add_map(p_map: dict)->None: add a dict of request params
        '''
        self._params.update(p_map)
        return

    def set_map(self, p_map):
        '''
        set_map(p_map: dict)->None: set params as p_map
        '''
        self._params = p_map
        return

    def clear_map(self):
        '''
        clear_map()->None: clear all params
        '''
        self._params.clear()
        return

    pass
