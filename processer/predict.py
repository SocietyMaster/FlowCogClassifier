#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path

import model.prediction_model


class Core(object):
    def __init__(self, predict_model=None):
        self.predict_model = predict_model

    def predict(self, group):
        return self.predict_model.predict(group)

    def load(self, directory=None):
        if not directory:
            self.predict_model.load()
        else:
            if not self.predict_model:
                self.predict_model = model.prediction_model.PredictionModel()
            self.predict_model.load(
                decision_model_dir=os.path.join(directory, "decision"),
                feature_model_dir=os.path.join(directory, "feature"),
                similarity_model_dir=os.path.join(directory, "similarity"))
        return self

    def load_model(self, model):
        self.predict_model = model
        return self
