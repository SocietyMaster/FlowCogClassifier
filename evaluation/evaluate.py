#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Evaluator(object):
    @staticmethod
    def evaluation(analyzed_result, labels):
        logger = logging.getLogger()
        tp = 0
        tn = 0
        fp = 0
        fn = 0
        for i, result in enumerate(analyzed_result):
            tp += 1 if analyzed_result[i] > threshold and labels[i] else 0
            tn += 1 if analyzed_result[i] <= threshold and (
            not labels[i]) else 0
            fp += 1 if analyzed_result[i] > threshold and (not labels[i]) else 0
            fn += 1 if analyzed_result[i] <= threshold and labels[i] else 0
        logger.info("|TP: %3d | FN: %3d|" % (tp, fn))
        logger.info("|-----------------|")
        logger.info("|FP: %3d | TN: %3d|" % (fp, tn))
