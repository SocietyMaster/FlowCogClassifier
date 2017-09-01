#!/usr/bin/env python
# -*- coding: utf-8 -*-


class WordsFilter(object):
    def __init__(self, dictionary):
        self._dictionary = dictionary

    def filter(self, words):
        words = list(words)
        return [word for word in words if word in self._dictionary]
