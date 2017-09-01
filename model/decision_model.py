#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import os.path

import accessor.loader
import accessor.saver


class DecisionModel(object):
    def __init__(self):
        self._model = dict()
        self._tf_model = dict()
        self._tf_cnt = dict()

    def load(self, directory):
        model_path = os.path.join(directory, "model.dat")
        tf_model_path = os.path.join(directory, "tf.dat")
        tf_cnt_path = os.path.join(directory, "tf_cnt.dat")
        self._model = accessor.loader.PickleLoader.load(model_path)
        self._tf_model = accessor.loader.PickleLoader.load(tf_model_path)
        self._tf_cnt = accessor.loader.JsonLoader.load(tf_cnt_path)
        return self

    def save(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)
        model_path = os.path.join(directory, "model.dat")
        tf_model_path = os.path.join(directory, "tf.dat")
        tf_cnt_path = os.path.join(directory, "tf_cnt.dat")
        accessor.saver.PickleSaver.save(self._model, model_path)
        accessor.saver.PickleSaver.save(self._tf_model, tf_model_path)
        accessor.saver.JsonSaver.save(self._tf_cnt, tf_cnt_path)
        return self

    def __transform(self, tainted_group):
        """
        Model key formatter. To transform tainted group into a specific string
        to hash as model key.
        :param tainted_group
        :return keys to hash
        """

        return tainted_group.flow.raw

    def train(self, tainted_groups):
        samples = []
        labels = []
        for group in tainted_groups:
            samples.append(self.__transform(group))
            labels.append(group.label)

        for i, item in enumerate(samples):
            if item not in self._tf_model.keys():
                self._tf_model[item] = {}
                self._tf_cnt[item] = 0
            if labels[i] not in self._tf_model[item].keys():
                self._tf_model[item][labels[i]] = 0
            self._tf_model[item][labels[i]] += 1
            self._tf_cnt[item] += 1

        for item in self._tf_model.keys():
            if item not in self._model.keys():
                self._model[item] = {}
            for label, cnt in self._tf_model[item].items():
                if label not in self._model[item].keys():
                    self._model[item][label] = {}
                self._model[item][label] = self._tf_model[item][label] / float(
                    self._tf_cnt[item])

    def predict(self, tainted_group):
        sample = self.__transform(tainted_group)
        if sample not in self._model.keys():
            return None
        else:
            result = max(self._model[sample].iteritems(), key=lambda x: x[1])
            return (result[0]).name, result[1]
