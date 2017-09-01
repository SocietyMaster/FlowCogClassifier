#!/usr/bin/env python
# -*- coding: utf-8 -*-
import simplejson

from configs.common import Values


class Blob(object):
    def __init__(self, **kwargs):
        self.flow_text = kwargs["flow_text"]
        self.related_text = kwargs["related_text"]
        self.flow = kwargs["flow"]
        self.app_description = kwargs["app_description"]
        self.label = kwargs["label"]
        self.layout_string = kwargs["layout_strings"]
        self.file = kwargs["file"]
        self.original_obj = dict(kwargs)

    def __str__(self):
        return str(self.original_obj)

    def __eq__(self, other):
        cls_variables = [attr for attr in dir(self) if not callable(getattr(
            self, attr)) and not attr.startswith("__")]
        for var in cls_variables:
            if getattr(self, var) != getattr(other, var):
                return False
        return True


def init():
    path = Values.labeled_tainted_groups_benign_app
    demo_input_file = open(path, "r")
    content = simplejson.load(demo_input_file)
    demo_input_file.close()
    blobs = []
    for entry in content:
        blobs.append(Blob(**entry))
    print(len(blobs))
    blobs_set = set(blobs)
    print(len(blobs_set))
    for i in blobs_set:
        print i


if __name__ == '__main__':
    init()
