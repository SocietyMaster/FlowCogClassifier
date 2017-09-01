#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import logging
import logging.config
import os.path

import configs
import demos.data
import demos.evaluate
import demos.predict
import demos.train
import entity.taint


def main():
    logger = logging.getLogger(__name__)
    logger.info("Start demo")

    data = demos.data.complete_set(
        configs.Values.all_labeled_tainted_groups_latest_path)

    test_percentage = 0.5
    retrain = True
    shuffle = True
    seed = 999

    logger.debug("[Number] Total number of all inputs: {number}".format(
        number=len(data)))

    tainted_groups_train, tainted_groups_test = demos.data.split_set(
        data, test_percentage, shuffle=shuffle, seed=seed)
    if retrain:
        demos.train.train(tainted_groups_train, save_dir=(
            configs.Values.prediction_model_directory))
    predicted_groups = demos.predict.predict(tainted_groups_test, load_path=(
        configs.Values.prediction_model_directory))

    demos.evaluate.evaluate(predicted_groups)


if __name__ == '__main__':
    logging.config.dictConfig(configs.Values.log_init_config)
    logger = logging.getLogger(__name__)
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", help="train, evaluate or predict")
    parser.add_argument("--data_set", help="path of data set")
    parser.add_argument("--test_percentage", help=(
        "define percentage of test set. It is available when working at "
        "evaluation mode"))
    parser.add_argument("--model_dir", help=(
        "directory to save/load trained models"))
    parser.add_argument("--no_shuffle", dest="shuffle", action="store_false",
                        default=True, help="is shuffle")
    parser.add_argument("--retrain", action="store_true", default=False, help=(
        "retrain the module if has this argument. Otherwise load from the "
        "model directory"))

    # parser.add_argument("--enable_prediction_json_input",
    #                     dest="prediction_json_input",
    #                     action="store_true",
    #                     default=False, help="Enable Json file input and disable"
    #                                         "command line input. "
    #                                         "If enabled, data set will be load "
    #                                         "by parameter --data_set")
    parser.add_argument("--flow", help="flow string in command line. "
                                       "Used in prediction mode")
    parser.add_argument("--text", help="text string in command line. "
                                       "Used in prediction mode")

    args = parser.parse_args()

    data = demos.data.complete_set(args.data_set)
    data = data[:int(0.01 * len(data))]

    logger.info("[Retrain] " + str(args.retrain))
    if args.mode == "train":
        train, test = demos.data.split_set(groups=data, test_percentage=0.0,
                                           shuffle=args.shuffle)
        demos.train.train(train, args.model_dir)
    elif args.mode == "evaluate":
        model_dir = args.model_dir
        if not model_dir:
            model_dir = configs.Values.prediction_model_directory
            logger.warning("Use default model directory at " + str(
                model_dir))

        if not args.retrain:
            test = data
        else:
            test_percentage = args.test_percentage
            if not test_percentage:
                test_percentage = 0.25
                logger.warning("Use default percentage {test_percentage},"
                               " please use --test_percentage to indicate the"
                               " rate of test set")
            train, test = demos.data.split_set(groups=data,
                                               test_percentage=test_percentage,
                                               shuffle=args.shuffle)
            demos.train.train(train, model_dir)

        predicted = demos.predict.predict(test, model_dir)
        demos.predict.print_predict(predicted)
        demos.evaluate.evaluate(predicted)
    elif args.mode == "predict":
        if args.data_set:
            path = args.data_set
            if not os.path.exists(path):
                logger.error("Json input file doesn't exist")
                exit(1)
            test = demos.data.complete_set(path)
        else:
            flow = args.flow
            text = args.text
            if not flow:
                logger.error("Please use --flow to give a flow string")
                exit(1)
            if not text:
                logger.error("Please use --text to give a text string")
                exit(1)
            test = [entity.taint.Group(flow=args.flow, flow_text=args.text)]
        predicted = demos.predict.predict(test, args.model_dir)
        logger.info("[Predict] " + str(predicted[0].prediction))
