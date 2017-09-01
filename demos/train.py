#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging.config

import configs
import demos.data
import processer.train


def train(tainted_groups, save_dir=None):
    """Interface"""
    logger = logging.getLogger(__name__)
    logger.info("[Number] Total number of training set: {number}".format(
        number=len(tainted_groups)))

    core = processer.train.Core()
    core.train(tainted_groups)
    if save_dir:
        core.save(save_dir)
    return tainted_groups


def main(test_percentage=0.1, data_set_path=None, shuffle=False, save_dir=None):
    """Main example"""
    logger = logging.getLogger(__name__)
    logger.info("[Start] Start training")
    data = demos.data.complete_set(data_set_path)
    tainted_groups_train, tainted_groups_test = demos.data.split_set(
        data, test_percentage, shuffle=shuffle)
    train(tainted_groups_train, save_dir=(
        configs.Values.prediction_model_directory))


if __name__ == '__main__':
    logging.config.dictConfig(configs.Values.log_init_config)
    main(test_percentage=0.1)
