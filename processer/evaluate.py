#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from entity.taint import GroupLabel


class Core(object):
    def __int__(self):
        pass

    @staticmethod
    def _evaluate_scores(predicted_groups):
        predictions = [group.prediction for group in predicted_groups]
        TP = 0
        FN = 0
        FP = 0
        TN = 0
        for i, group in enumerate(predicted_groups):
            label = group.label.name
            prediction = predictions[i].name
            if prediction == GroupLabel.BENIGN.name and prediction == label:
                TP += 1
            elif prediction == GroupLabel.BENIGN.name and prediction != label:
                FP += 1
            elif prediction == GroupLabel.MALICIOUS.name and prediction == label:
                TN += 1
            elif prediction == GroupLabel.MALICIOUS.name and prediction != label:
                FN += 1
            else:
                raise ValueError()
        accuracy = float(TP + TN) / (TP + FN + FP + TN) if (
            TP + FN + FP + TN) else 0
        precision = float(TP) / (TP + FP) if TP + FP else 0
        recall = float(TP) / (TP + FN) if TP + FN else 0
        return {"tp": TP, "fn": FN, "fp": FP, "tn": TN, "accuracy": accuracy,
                "precision": precision, "recall": recall}

    @staticmethod
    def _logging_scores(scores):
        logger = logging.getLogger(__name__)
        TP = scores["tp"]
        FN = scores["fn"]
        FP = scores["fp"]
        TN = scores["tn"]
        accuracy = scores["accuracy"]
        precision = scores["precision"]
        recall = scores["recall"]
        logger.info("[Result] TP: {TP}, FN: {FN}, FP: {FP}, TN: {TN}".format(
            TP=TP, FN=FN, FP=FP, TN=TN))
        logger.info("[Accuracy]: {accuracy}".format(accuracy=accuracy))
        logger.info("[Precision]: {precision}".format(precision=precision))
        logger.info("[Recall]: {recall}".format(recall=recall))

    def _evaluate_category(self, predicted_groups):
        """Evaluate based on categories, such as number and accuracy for each
         category. Firstly split all prediction based on flows, then print each
         score."""
        logger = logging.getLogger(__name__)
        # predictions = [group.prediction for group in predicted_groups]
        categories = {}
        for i, group in enumerate(predicted_groups):
            # label = group.label.name
            # prediction = predictions[i].name
            source = group.flow.source.raw
            sink = group.flow.sink.raw
            if source not in categories.keys():
                categories[source] = []
            categories[source].append(group)
            if sink not in categories.keys():
                categories[sink] = []
            categories[sink].append(group)
        for point, groups in categories.items():
            logger.info("\n[Category] {point}".format(point=point))
            scores = self._evaluate_scores(groups)
            self._logging_scores(scores)

    def evaluate(self, predicted_groups):
        logger = logging.getLogger(__name__)

        self._evaluate_category(predicted_groups)

        scores = self._evaluate_scores(predicted_groups)
        logger.info("\n")
        self._logging_scores(scores)
