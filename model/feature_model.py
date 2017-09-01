#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os

from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.externals import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import ShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import LinearSVC

import accessor.loader
import accessor.saver


def to_dense(x):
    return x.todense()


class FeatureModel(object):
    def __init__(self):
        self._v_clf = None
        self._cv = None
        self._clf = None
        self._label_encoder = None
        self._params = None

    def load(self, directory):
        v_clf_path = os.path.join(directory, "v_clf.dat")
        model_path = os.path.join(directory, "clf.dat")
        encoder_path = os.path.join(directory, "label_encoder.dat")
        param_path = os.path.join(directory, "params.dat")
        self._v_clf = joblib.load(v_clf_path)
        self._clf = joblib.load(model_path)
        self._label_encoder = joblib.load(encoder_path)
        self._params = accessor.loader.JsonLoader.load(param_path)
        return self

    def save(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)
        v_clf_path = os.path.join(directory, "v_clf.dat")
        model_path = os.path.join(directory, "clf.dat")
        encoder_path = os.path.join(directory, "label_encoder.dat")
        param_path = os.path.join(directory, "params.dat")
        joblib.dump(self._v_clf, v_clf_path)
        joblib.dump(self._clf, model_path)
        joblib.dump(self._label_encoder, encoder_path)
        # with open(param_path, "w") as param_file:
        #     json.dump(self._params, param_file)
        accessor.saver.JsonSaver.save(self._params, param_path)
        return self

    def __transform(self, tainted_group):
        tmp_str = ""
        concerned = [tainted_group.flow_text, tainted_group.related_text,
                     tainted_group.app_description,
                     tainted_group.layout_strings,
                     tainted_group.flow.source, tainted_group.flow.sink]
        for item in concerned:
            if item.is_skip:
                continue
            else:
                tmp_str += item.text if item.text else ""
        return tmp_str

    def __transform_groups(self, tainted_groups):
        data = []
        raw_labels = []
        for tainted_group in tainted_groups:
            data.append(self.__transform(tainted_group))
            raw_labels.append(str(tainted_group.label))
        self._label_encoder = LabelEncoder().fit(raw_labels)
        labels = self._label_encoder.transform(raw_labels)
        return data, labels

    def train(self, tainted_groups):
        logger = logging.getLogger(__name__)
        gb_clf = Pipeline([
            ("vectorizer", CountVectorizer(stop_words="english",
                                           ngram_range=(1, 2))),
            ("tfidf", TfidfTransformer()),
            ("to_dense", FunctionTransformer(to_dense,
                                             accept_sparse=True)),
            ("gbc", GradientBoostingClassifier(n_estimators=200))
        ])
        # ab_clf = pipeline([
        #     ("vectorizer", countvectorizer(stop_words="english",
        #                                    ngram_range=(1, 2))),
        #     ("tfidf", tfidftransformer()),
        #     ("to_dense", functiontransformer(to_dense, accept_sparse=true)),
        #     ("gbc", gradientboostingclassifier(n_estimators=200))
        # ])

        ab_clf = Pipeline([
            ("vectorizer",
             CountVectorizer(stop_words="english", ngram_range=(1, 2))),
            ("tfidf", TfidfTransformer()),
            ("clf", AdaBoostClassifier(n_estimators=100))
        ])
        lsvc_clf = Pipeline([
            ("vectorizer", CountVectorizer(stop_words="english")),
            ("tfidf", TfidfTransformer()),
            ("classifier", LinearSVC())
        ])
        self._v_clf = VotingClassifier(estimators=[("gb", gb_clf),
                                                   ("lsvc", lsvc_clf)],
                                       voting="hard")
        self._cv = ShuffleSplit(n_splits=3, random_state=1)
        data, labels = self.__transform_groups(tainted_groups)
        self._params = {}
        self._clf = GridSearchCV(self._v_clf, self._params, cv=self._cv,
                                 n_jobs=8, verbose=10)
        self._clf.fit(data, labels)
        # self._clf = self._clf.fit()
        logger.debug("[Best Score]" + str(self._clf.best_score_))
        # means = self._clf.cv_results_['mean_test_score']
        # stds = self._clf.cv_results_['std_test_score']
        # for mean, std, params in zip(means, stds,
        #                              self._clf.cv_results_['params']):
        #     print("%0.3f (+/-%0.03f) for %r"
        #           % (mean, std * 2, params))

    def predict(self, tainted_group):
        # self.predict_proba(tainted_group)
        return self._label_encoder.inverse_transform(
            self._clf.predict([self.__transform(tainted_group)]))[0]

    # def predict_proba(self, tainted_group):
    #     logger = logging.getLogger(__name__)
    #     result = self._clf.predict_proba([self.__transform(tainted_group)])
    #     logger.debug("[Predict Probability]" + str(result))

    def score(self, tainted_groups):
        data, labels = self.__transform_groups(tainted_groups)
        try:
            print("score", self._clf.score(data, labels))
        except Exception as e:
            print(e)


class ChiSquareModel(object):
    pass
