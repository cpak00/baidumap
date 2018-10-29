# baidu api url
base_url = 'http://api.map.baidu.com/'

# baidu api return status
status_map = {
    '0': ['0', 'Ok', '正常'],
    '1': ['1', 'Internal Server Error', '服务器内部错误'],
    '2': ['2', 'Parameter Invalid', '请求参数非法'],
    '3': ['3', 'Verify Failure', '权限校验失败'],
    '4': ['4', 'Quota Failure', '配额校验失败'],
    '5': ['5', 'AK Failure', 'ak不存在或者非法'],
    '1xx': ['1xx', 'Service Forbidden', '服务禁用'],
    '2xx': ['2xx', 'Authority Forbidden', '无权限'],
    '3xx': ['3xx', 'Lack of Quota', '配额错误'],
    '4xx': ['4xx', 'Concurrent Over', '并发超限'],
    'xxx': ['xxx', 'Undefined Error', '未定义错误'],
}

# log mode
DEBUG = 0
INFO = 1
WARNING = 2
ERROR = 3
NONE = 4
