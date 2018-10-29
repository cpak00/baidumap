# Baidu Map Api

## Description

This module is an python sdk for baidu map. You are only required to write a few code to get an execllent effect. Also, this module may work on another map api after some modification

## Get Start

```bash
pip install baidumap
```

install with pip, requestes required only.

```python
from baidumap.api.handle import get_handle
from baidumap.object import BaiduMapObject

ak_key = 'ZAMW5usZMrVb9oY3YqGTLa2rRGYaq7GV'
raw_handler = get_handle(ak_key)

if __name__ == '__main__':
    '''
    # Agent Mode
    raw_handler = get_handle(ak_key)
    thu_main = BaiduMapObject(address='北京市清华大学紫荆园餐厅')
    thu_main.from_address(raw_handler)
    print('from address find location: \n%s' % thu_main)
    thu_main.from_location(raw_handler)
    print('from location find uid: \n%s' % thu_main)
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
    '''

    # complex sample

    # get zijing dormitory location from agent mode
    thu_main = BaiduMapObject(address='北京市清华大学紫荆宿舍')
    thu_main.from_address(raw_handler)
    thu_location = thu_main.get_property('location')
    print('起始坐标: %s' % (thu_location))

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
    names = result.get_property('on_station')
    print('提取出全部的on_station属性(地铁站名)')
    print(names)
```
