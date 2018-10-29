# -*- coding:utf-8 -*-
from baidumap.core.static import status_map
from baidumap.util.dict_tool import s_get


class Status(object):
    def __init__(self, code, msg_en, msg_zh):
        self.code = str(code)
        self.msg_en = str(msg_en)
        self.msg_zh = str(msg_zh)
        self.msg = str()
        return

    def __str__(self):
        msg = 'Status[code=%s, msg_en=%s, msg_zh=%s, msg=%s]'
        return msg % (self.code, self.msg_en, self.msg_zh, self.msg)

    def is_ok(self):
        return self.msg_en.upper() == 'OK'

    def is_unknown(self):
        return self.code.upper() == 'XXX'

    pass


def get_status(code):
    '''
    get_status(code)->Status:get status from code
    '''
    code = str(code)
    if code not in status_map:
        code = code[0] + 'xx'
        if code not in status_map:
            code = 'xxx'
    status_list = list(s_get(status_map, code))
    status = Status(*status_list)
    return status


def get_status_from_json(json):
    '''
    '''
    code = s_get(json, 'status', '')
    status = get_status(code)
    if 'msg' in json:
        status.msg = json['msg']
    elif 'message' in json:
        status.msg = json['message']
    return status
