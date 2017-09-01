#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import random

import accessor.loader
import configs
import entity.taint


def __tainted_groups_load(path):
    """
    :param path: load the given path if not None.
    :return: data loaded.
    """
    data = accessor.loader.JsonLoader.load(path)
    return [entity.taint.Group().parse_json(item) for item in data]


def train_set(path=None):
    """
    Load the training set.
    :param path: if path is not given. Otherwise load the file in given
    location. Default path is defined in Class Values.
    :return:
    """
    path = path or configs.Values.benign_labeled_tainted_groups_path
    data = __tainted_groups_load(path)
    return data


def test_set(path=None):
    """
    Load the test set.
    :param path: if path is not given. Otherwise load the file in given
    location. Default path is defined in Class Values.
    :return:
    """
    path = path or configs.Values.malicious_labeled_tainted_groups_path
    data = __tainted_groups_load(path)
    return data


def complete_set(path=None):
    """
    Load the whole set.
    :param path: if path is not given. Otherwise load the file in given
    location. Default path is defined in Class Values.
    :return:
    """
    path = path or configs.Values.all_labeled_tainted_groups_path
    data = __tainted_groups_load(path)
    return data


def split_set(groups, test_percentage, shuffle=False, seed=None):
    """
    Split the set into training set and test set.
    :param groups: data set to split, whose type is list of entity.taint.Group.
    :param test_percentage: the percentage of test set in given whole set.
    :param shuffle:
    :param seed:
    :return:
    """
    if type(test_percentage) is not float:
        raise TypeError("Type of test_percentage must be float.")
    if not (0.0 <= test_percentage <= 1.0):
        raise ValueError("Argument test_percentage must be in range 0.0 to 1.0")

    complete_data = groups
    if seed:
        random.seed(seed)
    if shuffle:
        random.shuffle(complete_data)
    slice_point = int(len(complete_data) * (1 - test_percentage))
    train_data = groups[:slice_point]
    test_data = groups[slice_point:]
    return train_data, test_data
