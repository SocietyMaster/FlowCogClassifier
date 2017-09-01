#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pickle

import simplejson as json


class BaseSaver(object):
    def __init__(self, *args, **kwargs):
        pass


class JsonSaver(BaseSaver):
    @staticmethod
    def save(obj, location, mode="w"):
        with open(location, mode=mode) as json_file:
            json.dump(obj, json_file)


class PickleSaver(BaseSaver):
    @staticmethod
    def save(obj, location, mode="wb"):
        with open(location, mode=mode) as pickle_file:
            pickle.dump(obj, pickle_file)
