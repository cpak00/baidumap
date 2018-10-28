# -*- coding:utf-8 -*-


class BaiduMapApiException(Exception):
    '''
    baidu map api base exception
    '''
    def __init__(self, msg=''):
        Exception.__init__(self, msg)
        self.baidumap_status_code = ''
        return
    pass


class HandleNotExistsError(BaiduMapApiException):
    '''
    handle not exists
    '''
    def __init__(self, msg=''):
        msg = '''The handle is not exists, \
please check the handle name and if there is a '/' in the end or not'''
        Exception.__init__(self, msg)
        return
    pass


class NetError(BaiduMapApiException):
    '''
    net connect error
    '''
    def __init__(self, msg='please check the net connection'):
        Exception.__init__(self, msg)
        return
    pass


class OtherError(BaiduMapApiException):
    '''
    error which can not be recognized
    '''
    def __init__(self, msg=''):
        '''
        baidu map api error code: xxx
        '''
        Exception.__init__(self, msg)
        self.baidumap_status_code = 'xxx'
        return
    pass


def get_exception(status):
    '''
    get exception from code
    '''
    if status.is_unknown():
        return OtherError(status.msg_en)
    else:
        return BaiduMapApiException(status.msg or status.msg_en)
