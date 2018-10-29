# -*- coding:utf-8 -*-


def s_get(p_map, p_key, p_default=None):
    '''
    s_get(p_map, p_key, p_default)->p_map[p_key] or p_default
    '''
    try:
        return p_map[p_key]
    except Exception:
        return p_default


def s_set(p_map, p_key, p_value):
    '''
    s_set(p_map, p_key, p_value)->None
    '''
    try:
        p_map[p_key] = p_value
    finally:
        return


def s_sets(p_map, p_key_f, p_key_b, p_value):
    '''
    s_sets(p_map, p_key_f, p_key_b, p_value)->None
    '''
    try:
        if p_key_f not in p_map:
            p_map[p_key_f] = {p_key_b: p_value}
        else:
            p_map[p_key_f][p_key_b] = p_value
    except:
        return


def s_merge(map_a, map_b):
    '''
    s_merge(map_a, map_b)->None: merge map_b to map_a, won't cover
    '''
    try:
        for key_b in map_b:
            value = s_get(map_b, key_b)
            if key_b in map_a:
                s_merge(map_a[key_b], map_b[key_b])
            else:
                map_a[key_b] = value
    except:
        return


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
    if p_map is not None and p_key in p_map:
        p_value = p_map[p_key]
        p_map.remove(p_key)
        return p_value
    else:
        return p_default
