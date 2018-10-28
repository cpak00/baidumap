# -*- coding:utf-8 -*-


def s_get(p_map, p_key, p_default=None):
    '''
    s_get(p_map, p_key, p_default)->p_map[p_key] or p_default
    '''
    if p_map and p_key in p_map:
        return p_map[p_key]
    else:
        return p_default


def s_append(p_map, p_key, p_list):
    '''
    s_append(p_map, p_key, p_list)->None: save append a list
    '''
    if not isinstance(s_get(p_map, p_key), list):
        p_map[p_key] = p_list
    else:
        p_map[p_key].append(p_list)


def s_remove(p_map, p_key, p_default=None):
    '''
    s_remove(p_map, p_key)->p_value
    '''
    if p_map and p_key in p_map:
        p_value = p_map[p_key]
        p_map.remove(p_key)
        return p_value
    else:
        return p_default
