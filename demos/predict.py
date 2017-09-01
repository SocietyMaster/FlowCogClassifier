#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import logging.config

import configs
import demos.data
import processer.predict


def print_predict(predicted):
    logger = logging.getLogger(__name__)
    logger.info("[Result] Predict result")
    for i, group in enumerate(predicted):
        logger.info("[Id] {id}".format(id=i))
        logger.info("[Input] {group}".format(group=str(group)))
        logger.info("[Predicted]  {predicted}".format(
            predicted=predicted[i].prediction))
        logger.info("[Actual] {result}".format(result=group.label.name))


def predict(tainted_groups, load_path=None):
    """Interface"""
    logger = logging.getLogger(__name__)
    logger.debug("[Number] Total number to predict: {number}".format(
        number=len(tainted_groups)))
    load_path = load_path or configs.Values.prediction_model_directory
    core = processer.predict.Core()
    core = core.load(load_path)

    predicted = core.predict(tainted_groups)

    return predicted


def main():
    logger = logging.getLogger(__name__)
    logger.info("[Start] Start prediction")
    test_percentage = 0.1
    data = demos.data.complete_set(
        configs.Values.all_filtered_labeled_tainted_groups_path)
    tainted_groups_train, tainted_groups_test = demos.data.split_set(
        data, test_percentage, shuffle=False)
    predict(tainted_groups_train, load_path=(
        configs.Values.prediction_model_directory))


if __name__ == '__main__':
    logging.config.dictConfig(configs.Values.log_init_config)
    main()
