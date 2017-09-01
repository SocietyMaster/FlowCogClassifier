#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

import configs
import handler.behavior
import handler.taint
import model.decision_model
import model.feature_model
import model.similarity_model
from entity.taint import GroupLabel


class PredictionModel(object):
    def __init__(self):
        self.decision_model = model.decision_model.DecisionModel()
        self.feature_model = model.feature_model.FeatureModel()
        self.similarity_model = model.similarity_model.SimilarityModel()

        self._hyper_parameters = None

    def train(self, tainted_groups):
        logger = logging.getLogger(__name__)
        logger.info("[Train] start to train decision model")
        self.decision_model.train(tainted_groups)
        logger.info("[Train] start to train feature model")
        self.feature_model.train(tainted_groups)
        logger.info("[Train] start to train similarity model")
        self.similarity_model.train(tainted_groups)

    def save(self,
             decision_model_directory=configs.Values.decision_model_directory,
             feature_model_directory=configs.Values.feature_model_directory,
             similarity_model_directory=(
                     configs.Values.similarity_model_directory)):
        self.decision_model.save(decision_model_directory)
        self.feature_model.save(feature_model_directory)
        self.similarity_model.save(similarity_model_directory)
        return self

    def load(self, decision_model_dir=configs.Values.decision_model_directory,
             feature_model_dir=configs.Values.feature_model_directory,
             similarity_model_dir=configs.Values.similarity_model_directory):
        self.decision_model = self.decision_model.load(decision_model_dir)
        self.feature_model = self.feature_model.load(feature_model_dir)
        self.similarity_model = self.similarity_model.load(
            similarity_model_dir)
        return self

    def predict(self, tainted_groups):
        logger = logging.getLogger(__name__)
        raw_groups_handler = handler.taint.RawGroupsHandler()
        group_behavior_handler = handler.behavior.GroupsBehaviorHandler()
        # print(groups)
        tainted_groups = raw_groups_handler.process(tainted_groups)
        tainted_groups = group_behavior_handler.process(tainted_groups)

        for i, group in enumerate(tainted_groups):
            decision_result = self.decision_model.predict(group)
            feature_result = self.feature_model.predict(group)
            similarity_result = self.similarity_model.predict(group)
            # logger.debug("[Decision Result] " + str(decision_result))
            # logger.debug("[Feature Result] " + str(feature_result))
            # logger.debug("[Similarity Result] " + str(similarity_result))
            # logger.debug("[Label] " + str(group.label.name))

            is_decision_result_valid = False
            is_similarity_result_valid = False
            if decision_result and decision_result[1] > 0.99:
                decision_result = decision_result[0]
                is_decision_result_valid = True
            # TODO: Threshold
            if similarity_result and abs(similarity_result - 0) < 0.5:
                similarity_result = (GroupLabel.MALICIOUS.name if (
                        similarity_result) < 0 else GroupLabel.BENIGN.name)
                is_similarity_result_valid = True
            if is_decision_result_valid and is_similarity_result_valid and (
                        decision_result == similarity_result) and (
                        feature_result != similarity_result):
                result = GroupLabel[similarity_result]
            elif is_decision_result_valid and decision_result != (
                    feature_result):
                result = GroupLabel[feature_result.split(".")[1]]
            else:
                result = GroupLabel[feature_result.split(".")[1]]
            # print(result)
            tainted_groups[i].prediction = result
        return tainted_groups
