#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging.config

import configs.common
import demos.data
import demos.predict
import demos.train
import processer.evaluate
import processer.predict
import processer.train


def evaluate(predicted_groups):
    # logger = logging.getLogger(__name__)
    evaluate_core = processer.evaluate.Core()
    evaluate_core.evaluate(predicted_groups)


def train_and_predict(tainted_groups, test_percentage=0.75, retrain=True,
                      shuffle=False, seed=None):
    logger = logging.getLogger(__name__)

    logger.debug("[Number] Total number of all inputs: {number}".format(
        number=len(tainted_groups)))

    tainted_groups_train, tainted_groups_test = demos.data.split_set(
        tainted_groups, test_percentage, shuffle=shuffle, seed=seed)
    if retrain:
        demos.train.train(tainted_groups_train, save_dir=(
            configs.Values.prediction_model_directory))
    predicted_groups = demos.predict.predict(tainted_groups_test, load_path=(
        configs.Values.prediction_model_directory))
    return predicted_groups


def main():
    logger = logging.getLogger(__name__)
    logger.debug("Start evaluation")
    data = demos.data.complete_set(
        configs.Values.all_labeled_tainted_groups_latest_path)
    test_percentage = 0.5
    retrain = True
    shuffle = True
    seed = 999
    predicted_groups = train_and_predict(
        data, test_percentage=test_percentage,
        retrain=retrain, shuffle=shuffle,
        seed=seed)
    evaluate(predicted_groups)


if __name__ == '__main__':
    logging.config.dictConfig(configs.Values.log_init_config)
    main()
