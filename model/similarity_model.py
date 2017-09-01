#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import numpy as np
# import scipy.spatial.distance
#
# from pattern.singleton import Singleton
# from gensim.models import Word2Vec
# # from gensim.models import KeyedVectors
import logging
import operator
import os
import os.path
from collections import OrderedDict

import accessor.loader
import accessor.saver
import handler.similarity
import processer.scene


class SimilarityModel(object):
    def __init__(self, model=None):
        self._embedding_model = model or processer.scene.Scene().embedding_model
        self.threshold = -1
        self._similarity_handler = None

    def process(self, group):
        if not self._embedding_model:
            self._embedding_model = processer.scene.Scene().embedding_model
        if not self._similarity_handler:
            self._similarity_handler = (
                handler.similarity.HybridSimilarityHandler(
                    self._embedding_model))
        similarities = [0]
        tainted_texts = [group.flow_text, group.related_text,
                         group.app_description, group.layout_strings]
        tainted_points = [group.flow.source, group.flow.sink]
        for i in range(len(tainted_texts)):
            if tainted_texts[i].is_skip:
                continue
            for j in range(len(tainted_points)):
                similarities.append(self._similarity_handler.process(
                    tainted_texts[i], tainted_points[j]))
        return max(similarities)

    def train(self, tainted_groups):
        logger = logging.getLogger(__name__)
        self._embedding_model = processer.scene.Scene().embedding_model
        similarity_handler = handler.similarity.HybridSimilarityHandler(
            self._embedding_model)
        self._similarity_handler = similarity_handler

        results = []
        for group in tainted_groups:
            similarity = self.process(group)
            results.append(similarity)

        group_and_results = dict({k: v for k, v in zip(tainted_groups,
                                                       results)})
        group_and_results = OrderedDict(sorted(group_and_results.items(),
                                               key=operator.itemgetter(1)))
        correct_cnt = []
        thresholds = []
        for i in range(0, len(group_and_results)):
            last_value = i if i == 0 else group_and_results.items()[i - 1][1]
            next_value = group_and_results.items()[i][1]
            thresholds.append(float(last_value + next_value) / 2)
            correct_cnt.append(0)
            for group, result in group_and_results.items():
                if (group.label.value == 0 and result < thresholds[i]) or (
                                group.label.value == 1 and (
                                    result >= thresholds[i])):
                    correct_cnt[i] += 1
        # print(len(group_and_results))
        # print(correct_cnt)
        max_cnt = 0
        max_i = 0
        for i in range(len(correct_cnt)):
            if correct_cnt[i] > max_cnt:
                max_cnt = correct_cnt[i]
                max_i = i
            elif correct_cnt[i] == max_cnt:
                if abs(thresholds[i] - 0.5) > abs(thresholds[max_i] - 0.5):
                    max_cnt = correct_cnt[i]
                    max_i = i
        self.threshold = thresholds[max_i]
        logger.debug("[Similarity Threshold]" + str(self.threshold))

    def save(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)
        threshold_path = os.path.join(directory, "threshold.dat")
        accessor.saver.JsonSaver.save(self.threshold, threshold_path)
        return self

    def load(self, directory):
        threshold_path = os.path.join(directory, "threshold.dat")
        self.threshold = accessor.loader.JsonLoader.load(threshold_path)
        return self

    def load_model(self, model):
        self._embedding_model = model
        return self

    def predict(self, tainted_group):
        if not self.threshold:
            return None
        result = self.process(tainted_group)
        distance = result - self.threshold
        result = distance / float(self.threshold if distance < 0 else (
            1 - self.threshold))
        return result
