#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import logging.config
import os
import time

import requests
from accessor.variables import Variables
from bs4 import BeautifulSoup
from objects.tainted_objects import TaintedClassInfo
from scene import Scene

from accessor import Persister
from accessor.tainted_raw import TaintedRawLoader
from handler.behavior import BehaviorHandler
from handler.taint import TaintedClassInfoHandler


def find_longest_package(class_name, package_list):
    max_length = 0
    package_name = ""
    for package in package_list:
        if not class_name.startswith(package):
            continue
        if max_length < len(package):
            max_length = len(package)
            package_name = package
    return package_name


def get_package_list(path, update=False):
    if not update and os.path.exists(path):
        with open(path, "r") as input_file:
            package_names = [package.strip() for package in (
                input_file.readlines())]
        return package_names
    else:
        response = requests.get(
            "https://developer.android.com/reference/packages.html")
        bs = BeautifulSoup(response.text, "lxml")
        android_packages = bs.select("div[class='dac-reference-nav'] ul li a")
        package_names = [package.text.strip() for package in (
            android_packages)]
        with open(path, "w") as output_file:
            for tag in package_names:
                output_file.write(tag + "\n")
        return package_names


def get_description_dict(class_names, update=False):
    logger = logging.getLogger()
    class_description_dict_path = Variables.android_class_description_dict
    if not update and os.path.exists(class_description_dict_path):
        logger.debug("Get class descriptions locally")
        return Persister.json_load(class_description_dict_path)

    logger.debug("Downloading class description from Internet")
    android_package_list = Variables.android_package_list
    package_list = get_package_list(android_package_list)
    class_name_description_dict = {}
    for cls in class_names:
        logger.info(cls)
        prefix = "https://developer.android.com/reference/"
        suffix = ".html"
        package_name = find_longest_package(cls, package_list)
        class_name = cls.replace(package_name, "")[1:]
        if not package_name:
            url = prefix + "/".join(cls.split(".")) + suffix
            response = requests.get(url)
            time.sleep(1)
            if not response.ok:
                logger.error(url, "connect failed")
                continue
            bs = BeautifulSoup(response.text, "lxml")
            descriptions = bs.select("div[class='jd-descr'] p")
        else:
            url = prefix + "/".join(package_name.split(".") + [class_name]) + (
                suffix)
            response = requests.get(url)
            time.sleep(1)
            bs = BeautifulSoup(response.text, "lxml")
            descriptions = bs.select("#jd-content hr + p")
        if len(descriptions) > 0:
            class_name_description_dict[cls] = "".join(
                descriptions[0].text.splitlines())
        else:
            class_name_description_dict[cls] = ""
    Persister.json_save(class_name_description_dict,
                        class_description_dict_path)
    return class_name_description_dict


def get_class_description_behaviors(cls_desc_dict):
    cls_behaviors_dict = {}
    for cls, desc in cls_desc_dict.items():
        behavior_handler = BehaviorHandler()
        behaviors = behavior_handler.process(desc)
        cls_behaviors_dict[cls] = behaviors
    return cls_behaviors_dict


def init():
    sources_and_sinks_path = Variables.sources_and_sinks
    tainted_class_info_path = Variables.tainted_class_info_path
    tainted_classes = TaintedRawLoader.get_sources_sinks(sources_and_sinks_path)
    cls_desc_dict = get_description_dict(tainted_classes, update=True)
    cls_behaviors_dict = get_class_description_behaviors(cls_desc_dict)
    tainted_class_infos = []
    for cls in tainted_classes:
        print(cls, type(cls_behaviors_dict[cls]))
        tainted_class_infos.append(TaintedClassInfo(
            cls, cls_desc_dict[cls], cls_behaviors_dict[cls]))
    handler = TaintedClassInfoHandler()
    Persister.json_save(handler.objects_to_json(tainted_class_infos),
                        tainted_class_info_path)


if __name__ == '__main__':
    logging.config.dictConfig(Variables.log_init_config)
    init()
    Scene().server.stop()
