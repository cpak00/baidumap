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

ak_key = 'ZAMW5**********************'  # you need to use your own ak key

if __name__ == '__main__':
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
        region='北京',
        )
    print(placeser.run(max_page_num=1, max_result_num=15)['results'])

    circleser = get_handle(
        ak_key,
        'place/v2/search',
        is_list=True,
        query='医院'
    )

    location = thu_main.get_property('location')
    print(location)
    circleser.set_params(radius=2000, location=location)
    print(circleser.run(max_result_num=30))
```
