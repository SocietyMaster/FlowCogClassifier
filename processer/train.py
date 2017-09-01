#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os
import os.path

import handler.behavior
import handler.taint
import model.prediction_model


class Core(object):
    def __init__(self):
        logger = logging.getLogger()
        self.predict_model = model.prediction_model.PredictionModel()

    def train(self, groups):
        raw_groups_handler = handler.taint.RawGroupsHandler()
        group_behavior_handler = handler.behavior.GroupsBehaviorHandler()
        groups = raw_groups_handler.process(groups)
        groups = group_behavior_handler.process(groups)

        self.predict_model.train(groups)

    def save(self, directory=None):
        if not directory:
            self.predict_model.save()
        else:
            if not os.path.exists(directory):
                os.makedirs(directory)
            self.predict_model.save(
                decision_model_directory=os.path.join(directory, "decision"),
                feature_model_directory=os.path.join(directory, "feature"),
                similarity_model_directory=os.path.join(directory,
                                                        "similarity"))
        return self
