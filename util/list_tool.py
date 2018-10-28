# -*- coding:utf-8 -*-


def s_remove(p_list, p_value, p_default=None):
    '''
    s_remove(p_list, p_key)->p_value
    '''
    if p_list and p_value in p_list:
        p_list.remove(p_value)
        return p_value
    else:
        return p_default
