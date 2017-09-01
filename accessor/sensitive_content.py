#!/usr/bin/env python
# -*- coding: utf-8 -*-


def get_sensitive_contents(path):
    """
    Sensitive content is to identify the words or phrase that may
    be concerned by privilege.
    :param path:
    :return:
    """
    with open(path, "r") as input_file:
        content = input_file.readlines()
    content = [item.strip() for item in content if item.strip()]
    return content
