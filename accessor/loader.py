#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pickle

import simplejson as json


class BaseLoader(object):
    def __init__(self, *args, **kwargs):
        pass


class JsonLoader(BaseLoader):
    @staticmethod
    def load(location, mode="r"):
        with open(location, mode=mode) as json_file:
            obj = json.load(json_file)
        return obj


class PickleLoader(BaseLoader):
    @staticmethod
    def load(location, mode="rb"):
        with open(location, mode=mode) as pickle_file:
            obj = pickle.load(pickle_file)
        return obj
