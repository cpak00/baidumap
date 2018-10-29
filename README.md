# Baidu Map Api

## Description

This module is an python sdk for baidu map. You are only required to write a few code to get an execllent effect. Also, this module may work on another map api after some modification

## Get Start

```bash
pip install baidumap
```

install with pip, requestes required only.

 test.py
```python
from baidumap.api.handle import get_handle
from baidumap.object import BaiduMapObject

ak_key = 'ZAMW5******************'
raw_handler = get_handle(ak_key)

if __name__ == '__main__':
    # Agent Mode
    raw_handler = get_handle(ak_key)
    thu_main = BaiduMapObject(address='北京市清华大学紫荆园餐厅')
    thu_main.from_address(raw_handler)
    print('from address find location: %s' % thu_main.get_property('location'))
    print('from address find location: %s' % thu_main.get_properties(
        ['lat', 'lng'], p_defaults={'lat': '-1',
                                    'lng': '-1'}))
    thu_main.from_location(raw_handler)
    print('from location find uid: %s' % thu_main.get_property('uid'))
    print('and its name: %s' % thu_main.get_property('name'))

    find_location = thu_main.get_properties(
        ['uid', 'name'], p_defaults={'uid': '', 'name': ''})
    print('from location find uid and name: %s' % find_location)

    for index in find_location:
        thu_main.from_json(find_location[index])
        thu_main.from_uid(raw_handler, detail=True)
        print('from uid find info:\n%s' % thu_main)

    # Factory Mode
    iplocer = get_handle(ak_key, 'location/ip')
    iplocer.set_params()
    print(iplocer.run(collect_keys=['address', 'content'])['address'])

    placeser = get_handle(
        ak_key,
        'place/v2/search',
        is_list=True,
        query='ATM机',
        tag='银行',
        region='北京', )
    print(
        placeser.run(page_size=20, max_page_num=1, max_result_num=15)[
            'results'])

    # complex sample

    # get zijing dormitory location from agent mode
    thu_main = BaiduMapObject(address='北京市清华大学紫荆宿舍')
    thu_main.from_address(raw_handler)
    thu_location = thu_main.get_property('location')
    print('---\n\n起始坐标: %s' % (thu_location))

    # get circle search handle from factory mode
    # sort by distance
    circleser = get_handle(
        ak_key,
        'place/v2/search',
        is_list=True,
        query='火车站',
        scope=2,
        filter='sort_name:distance|sort_rule:1')

    circleser.set_params(radius=10000, location=thu_location)
    nearest_station = circleser.run(max_result_num=5)['results'][0]

    station_location = nearest_station.get_property('location')
    print('万米内最近的火车站: %s' % (nearest_station.get_property('name')))

    # get a handle to find road to hospital
    router = get_handle(ak_key, 'direction/v2/transit', is_list=True)

    router.set_params(origin=thu_location, destination=station_location)

    result = router.run()
    # print(repr(result))
    station = result.get_properties(['on_station', 'off_station'])
    print('提取出全部的on_station, off_station属性(地铁站名)')
    print(station)
```

## How to use BaiduMap Handle

### Factory Mode

Get handle from factory function `get_handle`
```python
from baidumap.api.handle import get_handle
```

Use name from [baidu map web api](http://lbsyun.baidu.com/index.php?title=webapi)

---

Sample

From [baidu map web api](http://lbsyun.baidu.com/index.php?title=webapi)

行政区划区域检索

http://api.map.baidu.com/place/v2/search?query=ATM机&tag=银行&region=北京&output=json&ak=您的ak //GET请求

The api path is `http://api.map.baidu.com/place/v2/search` (the / in the end or not is very important)

So this handle's name is `place/v2/search`(just remove the head of the api path)

```python
# ak_key is the authority key of the baidu map
# you need to apply for it from ('http://lbsyun.baidu.com/index.php?title=%E9%A6%96%E9%A1%B5')
ak_key = '********************'

# you can set params when get it from factory
# (the first two is not params, they are ak_key and handle's name)
# set is_list: true to get multi-page result
place_search = get_handle(ak_key, 'place/v2/search', is_list=True)

# then use method set_params() to set request parameter
place_search.set_params(query='ATM机', region='北京')

# use method run to get result

# you can limit the max_page_num(=-1 not limited), page_size(=10, limited by baidu mao), max_result_num(=-1 not limited) and interval(=0 second between each request(too frequently request will be block by baidu map and baidumap.api will raise baidumap.api.exceptions.BaiduMapApiException))

# place_search.run([max_page_num=-1[, max_result_num=-1[, page_size=10[, interval=0]]]])
atm_in_beijing = place_search.run(max_page_num=3, page_size=20, max_result_num=55, interval=0.5)

# get result
print(atm_in_beijing)
# get property(find mode)
# will return single result if there is only one property match
# will return dict result if there is a list of property match
print(atm_in_beijing.get_property('address'))
```

---

### Agent Mode

You can also use handle by agent mode

first you need to create a BaiduMapObject
```python
from baidumap.object import BaiduMapObject
```

