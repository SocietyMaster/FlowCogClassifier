#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path

from .defaults import DATA_ROOT
from .defaults import PROJECT_ROOT
from .defaults import SOURCE_ROOT
from .hyper_parameter import HyperParameter
from .logs import LoggerConfig


class Values(object):
    """
    Global variables is defined here.
    """
    project_root = PROJECT_ROOT
    source_root = SOURCE_ROOT
    data_root = DATA_ROOT

    # > hyper parameters
    hyper = HyperParameter
    # < hyper parameters

    # > application_database
    __data_application_database_path = os.path.join(data_root,
                                                    "application_database")
    database_filename = "PlainMetainfo.db"
    database_path = os.path.join(__data_application_database_path,
                                 database_filename)
    json_data_dump_path = os.path.join(__data_application_database_path,
                                       "fmt_data.json")
    # < application_database

    # > log_init
    log_init_config = LoggerConfig.config
    # < log_init

    # > resources
    __data_resources_path = os.path.join(data_root, "resources")
    # >> sources_and_sinks
    sources_and_sinks = os.path.join(
        __data_resources_path, "SourcesAndSinks.txt")
    # >> sorted_words
    sorted_words = os.path.join(
        __data_resources_path, "words_sorted_by_frequency.txt")
    # >> android_package_list
    android_package_list = os.path.join(
        __data_resources_path, "android_package_list.txt")
    # >> android_class_description_dict
    android_class_description_dict = os.path.join(
        __data_resources_path, "android_class_description_dict.json")
    # >> tainted_class_info_path
    tainted_class_info_path = os.path.join(
        __data_resources_path, "tainted_class_info.json")
    # >> stopwords
    stopwords_path = os.path.join(__data_resources_path, "stopwords.txt")
    # >> sensitive
    sensitive_content = os.path.join(__data_resources_path, "sensitive.txt")
    # < resources

    # > demo inputs
    __data_demo_inputs_path = os.path.join(data_root, "demo_inputs")

    all_labeled_tainted_groups_path = os.path.join(
        __data_demo_inputs_path, "all_fmt_new.txt")

    all_filtered_labeled_tainted_groups_path = os.path.join(
        __data_demo_inputs_path, "all_filtered.txt")

    all_labeled_tainted_groups_latest_path = os.path.join(
        __data_demo_inputs_path, "all_fmt_latest.txt")

    all_labeled_tainted_groups_description_path = os.path.join(
        __data_demo_inputs_path, "all_fmt_desc.txt")

    all_labeled_tainted_groups_flow_text_path = os.path.join(
        __data_demo_inputs_path, "all_fmt_flow_text.txt")

    benign_labeled_tainted_groups_path = os.path.join(
        __data_demo_inputs_path, "benign_fmt.txt")

    malicious_labeled_tainted_groups_path = os.path.join(
        __data_demo_inputs_path, "malicious_fmt.txt")

    # > demo inputs

    # > stanford
    __data_stanford_path = os.path.join(data_root, "stanford")
    # >> stanford corenlp
    stanford_corenlp_dir = os.path.join(
        __data_stanford_path, "stanford-corenlp-full")

    # > word2vec
    __data_word2vec_path = os.path.join(data_root, "word2vec")
    word2vec_model_path = os.path.join(__data_word2vec_path, "embedding.dat")

    # > permissions
    __data_permissions_path = os.path.join(data_root, "permissions")
    permissions_json_path = os.path.join(__data_permissions_path,
                                         "permissions.json")
    permissions_list_path = os.path.join(__data_permissions_path,
                                         "permissions_list.txt")

    # > models
    # > path to save models
    __data_model_path = os.path.join(data_root, "models")
    prediction_model_directory = __data_model_path
    decision_model_directory = os.path.join(prediction_model_directory,
                                            "decision")
    feature_model_directory = os.path.join(prediction_model_directory,
                                           "feature")
    similarity_model_directory = os.path.join(prediction_model_directory,
                                              "similarity")
    # < models
