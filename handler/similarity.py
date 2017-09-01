#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import math

import processer.scene
from base import BaseHandler
from configs.common import Values


class HybridSimilarityHandler(BaseHandler):
    def __init__(self, model=None, sensitive_content=None, word_filter=None):
        self._model = model or processer.scene.Scene().embedding_model
        self._sensitive_content = sensitive_content or (
            processer.scene.Scene().sensitive_content)
        self._words_filter = word_filter or (
            processer.scene.Scene().similarity_handler_stopwords)

    def _get_vector(self, word):
        return self._model.vector(word)

    def similar(self, text1, text2):
        if text1 in self._sensitive_content or text2 in self._sensitive_content:
            return 1 if text1 == text2 else 0
        return self._model.similar(text1, text2)

    def process(self, tainted_point, text):
        logger = logging.getLogger()
        pair_threshold = (
            Values.hyper.HybridSimilarityHandler_PAIR_THRESHOLD)
        action_threshold = (
            Values.hyper.HybridSimilarityHandler_ACTION_THRESHOLD)
        resource_threshold = (
            Values.hyper.HybridSimilarityHandler_RESOURCE_THRESHOLD)
        pair_weight = Values.hyper.HybridSimilarityHandler_PAIRWEIGHT

        text_behav = text.behaviors
        point_behav = tainted_point.behaviors
        if text_behav is not None:
            formatted_pairs = []
            for pair in text_behav.pairs:
                words = pair.split(" ")
                pair_action = words[0].strip()
                pair_resource = " ".join(words[1:]).strip()
                if pair_action not in self._words_filter and (
                        pair_resource) not in self._words_filter:
                    formatted_pairs.append(pair_action + pair_resource)
            text_behav.pairs = formatted_pairs

            text_behav.actions = [action.strip() for action in (
                text_behav.actions) if action.strip() not in self._words_filter]
            text_behav.resources = [resource.strip() for resource in (
                text_behav.resources) if resource.strip() not in (
                                        self._words_filter)]
        if point_behav is not None:
            point_behav_pairs = []
            for pair in point_behav.pairs:
                words = pair.split(" ")
                action = words[0]
                resource = " ".join(words[1:])
                if action not in self._words_filter and resource not in (
                        self._words_filter):
                    point_behav_pairs.append(pair)
            point_behav.pairs = point_behav_pairs
            point_behav.actions = [action for action in point_behav.actions if (
                action not in self._words_filter)]
            point_behav.resources = [resource for resource in (
                point_behav.resources) if (resource not in self._words_filter)]

        pair_score = 0
        pair_score_list = []
        for text_pair in text_behav.pairs:
            score = 0
            for point_pair in point_behav.pairs:
                tp = text_pair
                cp = point_pair
                if tp == cp:
                    score = 1
                    break
                sim = self.similar(tp, cp)
                # logger.debug("tp:%s, cp:%s, sim:%f" % (tp, cp, sim))
                sim = sim if sim > pair_threshold else 0
                if sim > score:
                    score = sim
            pair_score_list.append(score)
        pair_score_list = sorted(pair_score_list, reverse=True)
        for i, s in enumerate(pair_score_list):
            pair_score += pair_weight * math.pow(0.1, i) * s
        # logger.debug("pair_score: %f" % pair_score)

        action_score = 0
        action_score_list = []
        for text_action in text_behav.actions:
            score = 0
            for point_action in point_behav.actions:
                if text_action == point_action:
                    score = 1
                    break
                sim = self.similar(text_action, point_action)
                sim = sim if sim > action_threshold else 0
                if sim > score:
                    score = sim
            action_score_list.append(score)
        action_score_list = sorted(action_score_list, reverse=True)
        for i, s in enumerate(action_score_list):
            action_score += math.pow(0.5, i + 1) * math.sqrt(s)

        resource_score = 0
        resource_score_list = []
        for text_resource in text_behav.resources:
            score = 0
            for point_resource in point_behav.resources:
                if text_resource == point_resource:
                    score = 1
                    break
                sim = self.similar(text_resource, point_resource)
                # logger.debug("tr:%s, cr:%s, sim:%f" % (
                #     text_resource, point_resource, sim))
                sim = sim if sim > resource_threshold else 0
                if sim > score:
                    score = sim
            resource_score_list.append(score)
        resource_score_list = sorted(resource_score_list, reverse=True)
        for i, s in enumerate(resource_score_list):
            resource_score += math.pow(0.5, i + 1) * math.sqrt(s)

        max_score = max(action_score, resource_score)
        return max(pair_score, max_score)
