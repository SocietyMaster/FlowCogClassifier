#!/usr/bin/env python
# -*- coding: utf-8 -*-
import simplejson as json

from configs import Values

print(len(json.load(open(Values.all_filtered_labeled_tainted_groups_path))))

with open(Values.all_labeled_tainted_groups_path) as data_file:
    data = json.load(data_file)

print(len(data))
value_set = set()
filtered_data = []
represent = []
filtered_label = []
for item in data:
    to_hash_keys = ["flow_text", "flow", "related_text", "app_description"]
    str_to_hash = ""
    label = ""
    for i, (key, value) in enumerate(item.items()):
        if key in to_hash_keys:
            if not value:
                tmp_str = ""
            elif type(value) != str:
                tmp_str = value[0]
            else:
                tmp_str = value

            # if key == "flow":
            #     source, sink = [point.strip() for point in tmp_str.split("=>")]
            #     source_method, source_cls = source.split("@")
            #     sink_method, sink_cls = sink.split("@")
            #     tmp_str = " ".join([tmp_str, source, sink, source_method,
            #                         source_cls, sink_method, sink_cls])
            #     label = " ".join([source_cls, sink_cls, item["label"]])
            str_to_hash += tmp_str.strip()
    if str_to_hash in value_set:
        continue
    else:
        value_set.add(str_to_hash)
        filtered_data.append(item)
        represent.append(str_to_hash)
        # filtered_label.append(label)

data = filtered_data
print("Unique group can be used is {0}".format(len(data)))
for item in data:
    print(item)

# flow level

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import LinearSVC
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import ShuffleSplit
from sklearn.feature_extraction.text import TfidfVectorizer

flow_level_data = []
flow_level_label = []
for i, item in enumerate(data):
    # print("Point data: {0}".format(represent[i]))
    flow_level_data.append(represent[i])
    # print("Point label: {0}".format(data[i]["label"]))
    flow_level_label.append(data[i]["label"])

print("All label set:" + str(list(set(flow_level_label))))
label_encoder = LabelEncoder().fit(list(set(flow_level_label)))
encoded_labels = label_encoder.transform(flow_level_label)
flow_level_label = encoded_labels

# vectorizer = TfidfVectorizer()
# flow_level_data = vectorizer.fit_transform(flow_level_data)

test_percentage = 0.8

total = len(data)
slice_pos = int((1 - test_percentage) * total)
flow_level_data_train = flow_level_data[:slice_pos]
flow_level_label_train = flow_level_label[:slice_pos]
flow_level_data_test = flow_level_data[slice_pos:]
flow_level_label_test = flow_level_label[slice_pos:]

# clf = Pipeline([
#     ("vectorizer", CountVectorizer(stop_words="english")),
#     ("chi2", SelectKBest(chi2, k="all")),
# ("tfidf", TfidfTransformer()),
# ("classifier", LinearSVC())
# ("adaboost", AdaBoostClassifier())
#
# ])
#
# clf = AdaBoostClassifier(n_estimators=100)
# clf.fit(flow_level_data_train,  flow_level_label_train)
# predicted = clf.predict(flow_level_data_test)
#

# clf.fit(flow_level_data_train, flow_level_label_train)
# predicted = clf.predict(flow_level_data_test)
# from sklearn.metrics import accuracy_score
# print(accuracy_score(predicted, flow_level_label_test))

# print("n_samples: %d, n_features: %d" % x_train.shape)
# transformer = Pipeline([
#     ("vectorizer", CountVectorizer(stop_words="english")),
#     ("tfidf", TfidfTransformer()),
# ])




# gb_clf = GradientBoostingClassifier(n_estimators=100)

from sklearn.ensemble import VotingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import FunctionTransformer


def to_dense(x):
    return x.todense()


dt_clf = Pipeline([
    ("vect", TfidfVectorizer(stop_words="english")),
    ("clf", DecisionTreeClassifier())
])

gb_clf = Pipeline([
    ("vect", CountVectorizer(stop_words="english", ngram_range=(1, 2))),
    ("tfidf", TfidfTransformer()),
    ("todense", FunctionTransformer(to_dense, accept_sparse=True)),
    ("clf", GradientBoostingClassifier())
])
ab_clf = Pipeline([
    ("vect", CountVectorizer(stop_words="english", ngram_range=(1, 2))),
    ("tfidf", TfidfTransformer()),
    # ("todense", FunctionTransformer(lambda x: x.todense(), accept_sparse=True)),
    ("clf", AdaBoostClassifier())
])
lsvc_clf = Pipeline([
    ("vect", CountVectorizer(stop_words="english")),
    ("tfidf", TfidfTransformer()),
    ("clf", LinearSVC())
])
# svm_clf = Pipeline([
#     ("vectorizer", TfidfVectorizer(stop_words="english")),
#     ("classifier", SVC())
# ])

# dt_clf.fit(flow_level_data_train, flow_level_label_train)
# print(dt_clf.score(flow_level_data_test, flow_level_label_test))
# gb_clf.fit(flow_level_data_train, flow_level_label_train)
# print(gb_clf.score(flow_level_data_test, flow_level_label_test))
# ab_clf.fit(flow_level_data_train, flow_level_label_train)
# print(ab_clf.score(flow_level_data_test, flow_level_label_test))
# lsvc_clf.fit(flow_level_data_train, flow_level_label_train)
# print(lsvc_clf.score(flow_level_data_test, flow_level_label_test))

v_clf = VotingClassifier(estimators=[("gb", gb_clf), (
    "ab", ab_clf), ("lsvc", lsvc_clf)], voting="hard")
# clf.fit(flow_level_data_train, flow_level_label_train)
# print(clf.predict(flow_level_data_test))
# print(clf.score(flow_level_data_test, flow_level_label_test))

from sklearn.model_selection import GridSearchCV

params = {
    "gb__clf__n_estimators": [50, 100, 200],
    "ab__clf__n_estimators": [50, 100, 200],
}

cv = ShuffleSplit(n_splits=5)
clf = GridSearchCV(v_clf, params, cv=cv, n_jobs=8, verbose=10)
clf = clf.fit(flow_level_data, flow_level_label)
print(clf.best_score_)
print(clf.score(flow_level_data_test, flow_level_label_test))

means = clf.cv_results_['mean_test_score']
stds = clf.cv_results_['std_test_score']
for mean, std, params in zip(means, stds, clf.cv_results_['params']):
    print("%0.3f (+/-%0.03f) for %r"
          % (mean, std * 2, params))
