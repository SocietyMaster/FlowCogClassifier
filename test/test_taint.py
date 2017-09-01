#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import logging.config
import unittest

import simplejson as json

from configs import Values
from flowcog.entity.taint import Group
from flowcog.entity.taint import GroupLabel
from flowcog.entity.taint import Taint


class TestGroupLabel(unittest.TestCase):
    def test_members(self):
        self.assertIsNotNone(GroupLabel.MALICIOUS)
        self.assertIsNotNone(GroupLabel.BENIGN)
        self.assertIsNotNone(GroupLabel.UNKNOWN)
        self.assertEqual(GroupLabel.MALICIOUS.name, "MALICIOUS")
        self.assertEqual(GroupLabel.BENIGN.name, "BENIGN")
        self.assertEqual(GroupLabel.UNKNOWN.name, "UNKNOWN")
        self.assertEqual(GroupLabel.MALICIOUS.value, 0)
        self.assertEqual(GroupLabel.BENIGN.value, 1)
        self.assertEqual(GroupLabel.UNKNOWN.value, 2)


class TestGroup(unittest.TestCase):
    def setUp(self):
        logging.config.dictConfig(Values.log_init_config)
        self.raw = """{
        "flow_text": [
            "pan durisimo"
        ],
        "related_text": [
            "pan durisimo"
        ],
        "flow": "getString@android.database.Cursor => <init>@java.net.URL",
        "app_description": [
            "Discover the newest Tupperwarexae products, see the current menu of fun Tupperware party themes, learn the benefits of hosting a party or joining Tupperware as an independent Consultant, and connect via Facebook, Twitter and YouTube.  The official app of one of the most trusted names in housewares gives you a simple way to learn about whatu2019s new with a company thatu2019s been innovating for over 60 years.  Youu2019ll get notifications on special offers so you wonu2019t miss a chance to stock up and save. Also, you can find a Tupperware Consultant in your area who will be happy to help you plan your party and show you exactly how to get those amazing Host benefits. Donu2019t forget to ask them about how Tupperware has changed their lives, and learn about how it can change yours too."
        ],
        "label": "B",
        "layout_strings": [
            "Amount total:"
        ],
        "file": "out_com.Tupperware_US_EN.apk.txt"
         }"""
        self.dict = json.loads(self.raw)

    def test_construct_from_json_string(self):
        group = Group(self.raw)
        self.assertIsNotNone(group.filename)
        self.assertIsNotNone(group.flow)
        self.assertIsNotNone(group.flow_text)
        self.assertIsNotNone(group.related_text)
        self.assertIsNotNone(group.app_description)
        self.assertIsNotNone(group.layout_strings)
        self.assertIsNotNone(group.label)
        self.assertEqual(group.filename.raw, self.dict["file"])
        self.assertEqual(group.flow.raw, self.dict["flow"])
        self.assertEqual(group.flow_text.raw, self.dict["flow_text"])
        self.assertEqual(group.related_text.raw, self.dict["related_text"])
        self.assertEqual(group.app_description.raw,
                         self.dict["app_description"])
        self.assertEqual(group.layout_strings.raw, self.dict["layout_strings"])
        self.assertIsNotNone(group.label.raw, self.dict["label"])

    def test_dict_key_alias(self):
        group = Group(self.raw)
        self.assertIsNotNone(group.filename)
        self.assertEqual(group.filename.raw, self.dict["file"])

    def test_get_dict(self):
        group = Group(self.raw)
        self.assertEqual(group.dict["flow"], json.loads(self.raw)["flow"])

    def test_iterator(self):
        group = Group(self.raw)
        self.assertEqual(set(group.attribute_constructors().keys()),
                         set([attr for attr in group.attributes()]))

    def test_dict(self):
        group = Group(self.raw)
        self.assertEqual(len(group.dict), len(json.loads(self.raw)))

    def test_get_attribute(self):
        group = Group(self.raw)
        taint = Taint()
        for attr in group.attributes():
            self.assertIsNotNone(group[attr])
        self.assertEqual(len(group.attributes()),
                         len(group.attribute_constructors()))
        self.assertEqual(len(group.attributes(all=True)),
                         len(group.attributes()) + len(taint.attributes()))


if __name__ == '__main__':
    unittest.main()
