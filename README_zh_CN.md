
# 百度地图Web API Python模块

<!-- TOC -->

- [百度地图Web API Python模块](#百度地图web-api-python模块)
    - [描述](#描述)
    - [快速开始](#快速开始)
    - [调用方法](#调用方法)
        - [工厂模式](#工厂模式)
        - [代理模式](#代理模式)
    - [对象](#对象)
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
    - [错误&异常](#错误异常)
        - [BaiduMapApiException](#baidumapapiexception)
        - [HandleNotExistsError](#handlenotexistserror)
        - [NetError](#neterror)
        - [OtherError](#othererror)
    - [运行原理](#运行原理)
        - [core](#core)
            - [collector](#collector)
            - [controller](#controller)
            - [status](#status)
        - [util](#util)
            - [dict_tool & list_tool](#dict_tool--list_tool)
            - [url](#url)
    - [日志](#日志)
        - [config](#config)

<!-- /TOC -->

## 描述

本篇内容基于模块baidumap==1.2.4

百度地图Web API给了开发者们很大的自由发挥空间，百度地图官方提供了C， Java以及Android的开发SDK，但没有提供Python的开发包，本人虽然技术很有限，但是兴趣使然，就开发了第一个Python模块，用来简化百度地图API的调用流程

详细的内容参见[百度地图开放平台](http://lbsyun.baidu.com/index.php?title=webapi)

Github地址: https://github.com/cpak00/baidumap

作者: cpak00@github

邮箱: cymcpak00@gmail.com

## 快速开始

```bash
pip install baidumap
```

使用pip快速安装，Linux系统请使用pip3

我是Python3的忠实用户，而这个模块牵涉到字符编码的问题，所以Python2应该是无法使用的

下面是一端测试代码，涵盖了这个模块的基本功能
 test.py
```python
# -*- coding: utf-8 -*-
# 先导入百度地图开发包
from baidumap import config
from baidumap.api.handle import get_handle
from baidumap.object import BaiduMapObject

import logging

# 获取原始句柄
ak_key = 'ZAMW5**********************'
raw_handler = get_handle(ak_key)

# 获取日志记录器
FORMAT = "%(asctime)s %(thread)d %(message)s"
logging.basicConfig(format=FORMAT, datefmt="[%Y-%m-%d %H:%M:%S]")
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    # 日志记录配置（不是必要的）
    config.mode = config.value.DEBUG
    config.logger = logger

    # 代理模式示例
    print('---\nAgent Mode:\n')
    raw_handler = get_handle(ak_key)

	# 创建一个BaiduMapObject，并给它赋予一个初始值（可以用key=value）
	# 的模式赋予多个数据
    thu_main = BaiduMapObject(address='北京市清华大学紫荆园餐厅')
	
	# 调用代理函数，从address（地址）获取信息
	# 代理句柄raw_handler
	# 这里内部使用的是全球地理逆编码API
    thu_main.from_address(raw_handler)

	# 获取信息后，使用get_property函数获取对象内的参数
	# 详细获取数据只需要访问百度地图开放平台就可以完全查阅到
	# get_property可以递归获取参数，无需考虑字典的嵌套
    print('from address find location: %s' %
          thu_main.get_property('location')['location'])
	# get_properties可以同时获取多个参数并组合在一起
    print('from address find location: %s' % thu_main.get_properties(
        ['lat', 'lng'], p_defaults={'lat': '-1',
                                    'lng': '-1'}))
	# 从location（坐标）获取信息
    thu_main.from_location(raw_handler)
    print('\nfrom location find uid: %s' % thu_main.get_property('uid'))
    print('and its name: %s' % thu_main.get_property('name'))

    find_location = thu_main.get_properties(
        ['uid', 'name'], p_defaults={'uid': '',
                                     'name': ''})
    print('--\nfrom location find uid and name: %s' % find_location)

	# 从uid（唯一编码）获取建筑物（或区域）的详细信息
    for index in find_location:
        thu_main.from_json(find_location[index])
        thu_main.from_uid(raw_handler, detail=True)
        print('-\nfrom uid find info:\n%s' % thu_main)

    # 工厂模式示例
    print('---\nFactory Mode:\n')

	# 使用工厂函数生产出一个句柄
	# 句柄的第二个参数是句柄名称
	# 名称实际上就是API的URL的Path（路径）
    iplocer = get_handle(ak_key, 'location/ip')
	# 设置句柄参数
    iplocer.set_params()
    # 调用run（）会返回一个包含信息的BaiduMapObject对象
    print(
        iplocer.run(collect_keys=['address', 'content']).get_property(
            'address')['address'])

    print('---\n')
    # 句柄在生产的时候就可以赋予参数
    # is_list属性必须在生产的赋予
    # is_list在请求存在页码的时候需要为真
    placeser = get_handle(
        ak_key,
        'place/v2/search',
        is_list=True,
        query='ATM机',
        tag='银行',
        region='北京', )
    # run同样有可选参数，分别是每页包含数据条数，最大页数和最大结果数
    print(
        placeser.run(page_size=20, max_page_num=1, max_result_num=15)
        .get_property('address'))

    # 一个复杂的例子

    # 从地址获取坐标
    thu_main = BaiduMapObject(address='北京市清华大学紫荆宿舍')
    thu_main.from_address(raw_handler)
    thu_location = thu_main.get_property('location')['location']
    print('---\n\n起始坐标: %s' % (thu_location))

    # 获取一个句柄用于搜索
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

    # 获取一个用于规划路径的句柄
    router = get_handle(ak_key, 'direction/v2/transit', is_list=True)

    router.set_params(origin=thu_location, destination=station_location)

    result = router.run()
    station = result.get_properties(['on_station', 'off_station'])
    print('提取出全部的on_station, off_station属性(地铁站名)')
    print(station)
```

## 调用方法

### 工厂模式

从工厂函数获取句柄 `get_handle`
```python
from baidumap.api.handle import get_handle
```

使用从 [百度地图开放平台Web API文档](http://lbsyun.baidu.com/index.php?title=webapi)获取的API对应的URL来获取一个句柄的名称

---

样例

[百度地图Web API](http://lbsyun.baidu.com/index.php?title=webapi)

行政区划区域检索

http://api.map.baidu.com/place/v2/search?query=ATM机&tag=银行&region=北京&output=json&ak=您的ak //GET请求

这个API的URL是 `http://api.map.baidu.com/place/v2/search` (结尾有没有/很__重要__)

所以这个句柄的名字就是 `place/v2/search`(只要移除掉万维网前缀即可)

```python
# ak_key是百度地图开放平台的密钥
# 你需要从以下网址申请('http://lbsyun.baidu.com/index.php?title=%E9%A6%96%E9%A1%B5')
ak_key = '********************'

# 你可以设置从工厂函数生产句柄的时候设置参数
# (前两个不是参数，分别是ak和句柄名称)
# 把is_list设置为真的时候说明这是一个用于获取列表数据的句柄
place_search = get_handle(ak_key, 'place/v2/search', is_list=True)

# 然后设置API所需要的参数
place_search.set_params(query='ATM机', region='北京')

# 使用run（）来获取结果

# 你可以限制max_page_num(=-1 默认不限制), page_size(=10, 上下限由百度规定), max_result_num(=-1 默认不限制) and 请求间隔interval(=0 秒 (过于频繁的请求会被百度拒绝 并且 baidumap.api 会抛出 baidumap.api.exceptions.BaiduMapApiException异常))

# place_search.run([max_page_num=-1[, max_result_num=-1[, page_size=10[, interval=0]]]])
atm_in_beijing = place_search.run(max_page_num=3, page_size=20, max_result_num=55, interval=0.5)

# 获取结果
print(atm_in_beijing)
# 获取结果中的参数（自动深度搜索，无需关注字典的嵌套问题）
# 结果会返回一个字典
print(atm_in_beijing.get_property('address'))
```

---

### 代理模式

你也可以使用 __代理模式__

首先import **BaiduMapObject**和**Handle**
```python
from baidumap.object import BaiduMapObject,Handle
```

然后使用key=value的键值对（可以是多个）来构建对象
```python
thu_main = BaiduMapObject(address='北京市清华大学紫荆宿舍')
```

然后你需要创建一个包含*ak_key*的原始句柄
```python
raw_handle = Handle(ak_key)
```

最后你只需要调用代理函数代理上面获得的原始句柄就可以让**BaiduMapObject**获取数据
```python
# 调用地理解码
# 会在对象里填充坐标等信息
thu_main.from_address(handle)

# 地理编码调用
# 会填充根据坐标发现的周边建筑的uid和address等信息
# 这样做会返回一个list-like的百度地图对象
thu_main.from_location(handle)

# 创建一个带uid的百度地图对象
thu_main = BaiduMapObject(uid=thu_main.get_property('uid')[0].uid)

# 详细信息获取
# 从uid填充详细信息
thu_main.from_uid(handle, detail=True)
```

## 对象

### JsonLike

#### `__init__(json=dict(), **kwargs)`

>**JsonLike**对象可以被**list**或**dict**初始化, 你也可以通过声明**kwargs来替换掉一些参数

#### `__str__()`

>**JsonLike** 可以像*字典*那样被转换为*字符串*

#### `is_list()`

>**JsonLike**对象可能是 *dict-like*或*list-like*，取决于初始化它的对象

#### `get_property(p_key, p_default=None)`

>如果你想获取**JsonLike**的参数, 推荐这个函数, 返回*字典*.

>如果只有一个结果, 返回像这样的结果：{key: value}

>如果有多对结果, 会返回一个包含位置信息的*list-like*的*字典*

#### `get_properties(p_keys, p_defaults=None)`

>你可以将多个参数信息包含在一个*list-like*的*字典*

#### `set_property(p_key, p_value)`

>你不能用键值对的方式来设置<**JsonLike**>

>如果你用这种方式设置值, 如果*p_key*不在**JsonLike**中, 你不会得到任何结果
#### `keys()`

>返回**JsonLike**所有的键

#### `from_json(json, **kwargs)`

>从json数据重构**JsonLike**，可能是*字典* or *列表*, 可以使用*kwargs* 替换部分参数

#### `to_json()`

>以*字典*形式返回**JsonLike**

### Location(JsonLike)

#### `__str__()`

>位置对象会被转换成经度，纬度的格式

### BaiduMapObject(JsonLike)

#### `from_uid(handle, detail=False)`

>用uid搜索**BaiduMapObject**
>需要一个带ak密钥的原始句柄

#### `from_address(handle, detail=False)`

>用地址搜索**BaiduMapObject**
>需要一个带ak密钥的原始句柄

#### `from_location(handle, detail=False)`

>用坐标搜索**BaiduMapObject**
>需要一个带ak密钥的原始句柄

## 错误&异常

### BaiduMapApiException

>基类异常

>位置：baidumap.api.exception

### HandleNotExistsError

>继承**BaiduMapApiException**

>无效的句柄

>位置：baidumao.api.exception

### NetError

>继承**BaiduMapApiException**

>网络错误

>位置：baidumao.api.exception

### OtherError

>继承**BaiduMapApiException**

>无法识别的错误

>位置：baidumao.api.exception

## 运行原理

### core

>package baidumap.core

#### collector

#### controller

#### status

### util

>package baidumap.util

#### dict_tool & list_tool

一些安全操作数组和字典的函数

#### url

class **Url**

管理URL地址和参数

使用模块*requests* 来获取GET请求

## 日志

### config

*baidumap.config.mode*

value                | description
---------------------|------------------------
config.value.DEBUG   | 运行细节记录
config.value.INFO    | 重要运行语句
config.value.WARNING | 不安全的运行
config.value.ERROR   | 错误记录
config.value.NONE    | 不记录

*baidumap.config.filename*

value      | description
-----------|-------------
None       | 直接打印在控制台
**Logger** | 使用logging模块代理日志
