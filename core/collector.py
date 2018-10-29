# -*- coding:utf-8 -*-
from json.decoder import JSONDecodeError
from time import sleep

from baidumap.api.exceptions import HandleNotExistsError
from baidumap.core.status import get_status_from_json
from baidumap.util import log
from baidumap.util.dict_tool import s_append, s_get
from baidumap.util.list_tool import s_remove


class Collector:
    '''
    baidu api data collector
    '''

    def __init__(self, ak_key):
        self.ak_key = ak_key
        return

    def get_single_result(self, p_url, collect_keys=None):
        '''
        get_single_result(p_url)->status: Status, result: dict
        '''
        p_url.set_param('ak', self.ak_key)
        p_url.set_param('output', 'json')
        response = p_url.get()
        log.debug('requests GET: %s' % p_url)
        try:
            json = response.json()
        except JSONDecodeError:
            log.error('JSONDecodeError:\nraw:\n%s' % response.raw)
            raise HandleNotExistsError()
        result = dict()

        # default collect all
        if collect_keys is None:
            collect_keys = list(json.keys())
            # keys below are not information
            s_remove(collect_keys, 'status')
            s_remove(collect_keys, 'message')
            s_remove(collect_keys, 'msg')

        for key in collect_keys:
            result[key] = s_get(json, key, dict())

        status = get_status_from_json(json)
        log.debug('response status: %s' % status)
        return status, result

    def get_list_result(self,
                        p_url,
                        collect_keys=None,
                        page_size=10,
                        max_page_num=-1,
                        max_result_num=-1,
                        interval=0):
        '''
        get_list_result(p_url[, max_page_num[, max_result_num]])
        ->status: Status, result: list
        '''
        page_num = 0
        p_url.set_param('page_size', page_size)

        total_results = dict()
        status = None

        empty_flag = False  # use to check if there is a list not empty
        while page_num < max_page_num or max_page_num < 0:
            log.debug('page_num: %d' % page_num)

            empty_flag = True
            p_url.set_param('page_num', page_num)
            status, result = self.get_single_result(p_url, collect_keys)
            if not status.is_ok():
                return status, total_results
            else:
                # request Ok
                for key in result:
                    result_list = s_get(result, key)
                    if not isinstance(result_list, list):
                        total_results[key] = result_list
                        continue
                    else:
                        s_append(total_results, key, result_list)

                        # if there is a list not empty
                        current_num = len(result_list)
                        if current_num > 0:
                            empty_flag = False

                        total_list = s_get(total_results, key, list())
                        total_num = len(total_list)
                        if current_num == 0:
                            # iteration finish
                            continue
                        elif total_num > max_result_num and max_result_num > 0:
                            # iteration finish
                            total_results[key] = total_list[:max_result_num]
                            empty_flag = True
                            break

                # iterate or not
                if empty_flag:
                    break
                else:
                    sleep(interval)
                    page_num += 1
        return status, total_results

    pass
