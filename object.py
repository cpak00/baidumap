# -*- coding:utf-8 -*-
from baidumap.util.dict_tool import s_get


class JsonLike(object):
    def __init__(self, json=dict(), **kwargs):
        '''
        JsonLike Object
        '''
        self.from_json(json, **kwargs)

    def __str__(self):
        copy_dict = self.__dict__.copy()
        for key in copy_dict:
            value = s_get(copy_dict, key)
            copy_dict[key] = str(value)

        return str(copy_dict)

    def __repr__(self):
        return repr(self.__dict__)

    def __getitem__(self, key):
        return self.__dict__[key]

    def get_property(self, p_key, p_default=None):
        if p_key in self.__dict__:
            return s_get(self.__dict__, p_key, p_default)
        else:
            for key in self.__dict__:
                value = s_get(self.__dict__, key)
                if isinstance(value, JsonLike):
                    value = s_get(self.__dict__, key,
                                  JsonLike()).get_property(p_key, p_default)
                    if value is not None and value != p_default:
                        return value
            return p_default

    def set_property(self, p_key, p_value):
        if p_key in self.__dict__:
            self.__dict__[p_key] = p_value
        else:
            for key in self.__dict__:
                value = s_get(self.__dict__, key)
                if isinstance(value, JsonLike):
                    s_get(self.__dict__, key, JsonLike()).set_property(
                        p_key, p_value)
            return

    def from_json(self, json, **kwargs):
        self.__dict__ = dict()
        if isinstance(json, dict) or isinstance(json, JsonLike):
            json.update(kwargs)
            for key in json:
                value = s_get(json, key, '')
                if isinstance(value, list):
                    value = BaiduMapObject(value)
                elif isinstance(value, dict):
                    value = JsonLike(value)
                self.__dict__[key] = value
        elif isinstance(json, list):
            for index, key in enumerate(json):
                self.__dict__[index] = BaiduMapObject(key)

    def to_json(self):
        return self.__dict__

    pass


class Location(JsonLike):
    def __str__(self):
        lat = s_get(self.__dict__, 'lat', '-1')
        lng = s_get(self.__dict__, 'lng', '-1')
        return '%s,%s' % (lat, lng)

    def to_json(self):
        if 'lat' in self.__dict__ and 'lng' in self.__dict__:
            lat = s_get(self.__dict__, 'lat', '-1')
            lng = s_get(self.__dict__, 'lng', '-1')
        return {'lat': lat, 'lng': lng}

    pass


class BaiduMapObject(JsonLike):
    def __init__(self, *args, **kwargs):
        JsonLike.__init__(self, *args, **kwargs)

        # change location from JsonLike to Location
        location = self.get_property('location')
        if location:
            pre_location = location.to_json()
            self.set_property('location', Location(pre_location))

    def from_uid(self, handle=None, detail=False):
        # use handle to get detail info
        handle.set_name('place/v2/detail')
        uid = self.get_property('uid', '')
        if detail:
            scope = '2'
        else:
            scope = '1'
        handle.set_params(uid=uid, scope=scope)
        self.from_json(handle.run().to_json())
        return

    def from_address(self, handle=None):
        # use handle to get location
        handle.set_name('geocoder/v2/')
        address = self.get_property('address', '')
        handle.set_params(address=address)
        self.from_json(handle.run().to_json())
        return

    def from_location(self, handle=None):
        # use handle to get address
        handle.set_name('geocoder/v2/')
        location = self.get_property('location', '')
        handle.set_params(location=location)
        self.from_json(handle.run().to_json())
        return

    pass
