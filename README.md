# Baidu Map Api

<!-- TOC -->

- [Baidu Map Api](#baidu-map-api)
    - [Description](#description)
    - [Get Start](#get-start)
    - [Handle](#handle)
        - [Factory Mode](#factory-mode)
        - [Agent Mode](#agent-mode)
    - [Object](#object)
        - [JsonLike](#jsonlike)
            - [`__init__(json=dict(), **kwargs)`](#__init__jsondict-kwargs)
            - [`__str__()`](#__str__)
            - [`is_list()`](#is_list)
            - [`get_property(p_key, p_default=None)`](#get_propertyp_key-p_defaultnone)
            - [`get_properties(p_keys, p_defaults=None)`](#get_propertiesp_keys-p_defaultsnone)
            - [`set_property(p_key, p_value)`](#set_propertyp_key-p_value)
            - [`keys()`](#keys)
            - [`from_json(json, **kwargs)`](#from_jsonjson-kwargs)
            - [`to_json()`](#to_json)
        - [Location(JsonLike)](#locationjsonlike)
            - [`__str__()`](#__str__-1)
        - [BaiduMapObject(JsonLike)](#baidumapobjectjsonlike)
            - [`from_uid(handle, detail=False)`](#from_uidhandle-detailfalse)
            - [`from_address(handle, detail=False)`](#from_addresshandle-detailfalse)
            - [`from_location(handle, detail=False)`](#from_locationhandle-detailfalse)
    - [Exception](#exception)
        - [BaiduMapApiException](#baidumapapiexception)
        - [HandleNotExistsError](#handlenotexistserror)
        - [NetError](#neterror)
        - [OtherError](#othererror)
    - [How to work](#how-to-work)
        - [core](#core)
            - [collector](#collector)
            - [controller](#controller)
            - [status](#status)
        - [util](#util)
            - [dict_tool & list_tool](#dict_tool--list_tool)
            - [url](#url)
    - [Log](#log)
        - [config](#config)

<!-- /TOC -->

## Description

This module is an python sdk for baidu map. You are only required to write a few code to get an execllent effect. Also, this module may work on another map api after some modification

Author: cpak00@github

Email: cymcpak00@gmail.com

## Get Start

```bash
pip install baidumap
```

install with pip, requestes required only.

 test.py
```python
from baidumap import config
from baidumap.api.handle import get_handle
from baidumap.object import BaiduMapObject

import logging

# get raw handler
ak_key = 'ZAMW5**********************'
raw_handler = get_handle(ak_key)

# get logger
FORMAT = "%(asctime)s %(thread)d %(message)s"
logging.basicConfig(format=FORMAT, datefmt="[%Y-%m-%d %H:%M:%S]")
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    # log config(no necessary)
    config.mode = config.value.DEBUG
    config.logger = logger

    # Agent Mode
    print('---\nAgent Mode:\n')
    raw_handler = get_handle(ak_key)
    thu_main = BaiduMapObject(address='北京市清华大学紫荆园餐厅')
    thu_main.from_address(raw_handler)
    print('from address find location: %s' %
          thu_main.get_property('location')['location'])
    print('from address find location: %s' % thu_main.get_properties(
        ['lat', 'lng'], p_defaults={'lat': '-1',
                                    'lng': '-1'}))
    thu_main.from_location(raw_handler)
    print('\nfrom location find uid: %s' % thu_main.get_property('uid'))
    print('and its name: %s' % thu_main.get_property('name'))

    find_location = thu_main.get_properties(
        ['uid', 'name'], p_defaults={'uid': '',
                                     'name': ''})
    print('--\nfrom location find uid and name: %s' % find_location)

    for index in find_location:
        thu_main.from_json(find_location[index])
        thu_main.from_uid(raw_handler, detail=True)
        print('-\nfrom uid find info:\n%s' % thu_main)

    # Factory Mode
    print('---\nFactory Mode:\n')
    iplocer = get_handle(ak_key, 'location/ip')
    iplocer.set_params()
    print(
        iplocer.run(collect_keys=['address', 'content']).get_property(
            'address')['address'])

    print('---\n')
    placeser = get_handle(
        ak_key,
        'place/v2/search',
        is_list=True,
        query='ATM机',
        tag='银行',
        region='北京', )
    print(
        placeser.run(page_size=20, max_page_num=1, max_result_num=15)
        .get_property('address'))

    # complex sample

    # get zijing dormitory location from agent mode
    thu_main = BaiduMapObject(address='北京市清华大学紫荆宿舍')
    thu_main.from_address(raw_handler)
    thu_location = thu_main.get_property('location')['location']
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

    station_location = nearest_station.get_property('location')['location']
    print('万米内最近的火车站: %s' % (nearest_station.get_property('name')['name']))

    # get a handle to find road to hospital
    router = get_handle(ak_key, 'direction/v2/transit', is_list=True)

    router.set_params(origin=thu_location, destination=station_location)

    result = router.run()
    # print(repr(result))
    station = result.get_properties(['on_station', 'off_station'])
    print('提取出全部的on_station, off_station属性(地铁站名)')
    print(station)
```

## Handle

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
# will return a dict
print(atm_in_beijing.get_property('address'))
```

---

### Agent Mode

You can also use handle by __agent mode__

first. you need to import **BaiduMapObject**
```python
from baidumap.object import BaiduMapObject
```

second. you need to create a BaiduMapObject with some keys and values
```python
thu_main = BaiduMapObject(address='北京市清华大学紫荆宿舍')
```

then. you need to create a raw handle with *ak_key*
```python
raw_handle = get_handle(ak_key)
```

finally. you just call the agent method to fill the data of **BaiduMapObject**
```python
# geography decoder call
# it will fill Object with location
thu_main.from_address(handle)

# geography encoder call
# it will fill Object with address and uid found by location
# it will create a list-like BaiduMapObject
thu_main.from_location(handle)

# create a object with uid
thu_main = BaiduMapObject(uid=thu_main.get_property('uid')[0].uid)

# uid info call
# it will fill Object with detail info found by uid
thu_main.from_uid(handle, detail=True)
```

## Object

### JsonLike

#### `__init__(json=dict(), **kwargs)`

>**JsonLike** object can be inited with **list** or **dict**, you can replace some parameters by decalre *kwargs*

#### `__str__()`

>**JsonLike** object will be transfered as **str** just like **dict**

#### `is_list()`

>**JsonLike** object can be *dict-like* or *list-like* determined by which one init it

#### `get_property(p_key, p_default=None)`

>if you want to read value of **JsonLike**, this method is suggested, it will return a *dict*.

>if there is only one result, it will return *dict* as {key: value}

>if there are more results, it will return a *list-like* *dict* which contains location

#### `get_properties(p_keys, p_defaults=None)`

>you can combine two or more properties in one *list-like* *dict*

#### `set_property(p_key, p_value)`

>you can't set key-value using <**JsonLike**>[key]=value

>you are supposed to set property with this method, if there is no *p_key* in the **JsonLike** object, you can not set it with this method

#### `keys()`

>return the keys in the **JsonLike** object

#### `from_json(json, **kwargs)`

>reconstruct the **JsonLike** object by *dict* or *list*, can replace some properties by *kwargs* 

#### `to_json()`

>return *dict* in **JsonLike**

### Location(JsonLike)

#### `__str__()`

>location will be formatted as lat,lng

### BaiduMapObject(JsonLike)

#### `from_uid(handle, detail=False)`

>fill the **BaiduMapObject** by uid

>needs a handle with valid ak_key

#### `from_address(handle, detail=False)`

>fill the **BaiduMapObject** by address

>needs a handle with valid ak_key

#### `from_location(handle, detail=False)`

>fill the **BaiduMapObject** by location

>needs a handle with valid ak_key

## Exception

### BaiduMapApiException

>base exception

>in baidumap.api.exception

### HandleNotExistsError

>inherit from **BaiduMapApiException**

>handle name not valid

>in baidumao.api.exception

### NetError

>inherit from **BaiduMapApiException**

>net connection broken

>in baidumao.api.exception

### OtherError

>inherit from **BaiduMapApiException**

>error which can not be recognized

>in baidumao.api.exception

## How to work

### core

>package baidumap.core

#### collector

#### controller

#### status

### util

>package baidumap.util

#### dict_tool & list_tool

some safe operation functions

#### url

class **Url**

manager the params and url path

use package *requests* to get json by http request[GET]

## Log

### config

*baidumap.config.mode*

value                | description
---------------------|------------------------
config.value.DEBUG   | log detail information
config.value.INFO    | log important statement
config.value.WARNING | log unsafe statement
config.value.ERROR   | log error
config.value.NONE    | no log

*baidumap.config.filename*

value      | description
-----------|-------------
None       | directly record in shell
**Logger** | use module logging
