#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from enum import Enum


class TaintBase(object):
    pass


class Text(TaintBase):
    def __init__(self, raw_text):
        self.raw = raw_text
        self.text = None
        self.behaviors = None
        self.is_skip = False

        self.parsed_info = None
        self.parse_trees = None
        # self.json = None
        # self.dict = None

    def __str__(self):
        _str = list([])
        _str.append("flow_text={flow_text}".format(flow_text=self.text))
        _str.append("behaviors=%s" % self.behaviors)
        if self.behaviors:
            _str.append("behaviors.pairs=%s" % self.behaviors.pairs)
            _str.append("behaviors.actions=%s" % self.behaviors.actions)
            _str.append("behaviors.resources=%s" % self.behaviors.resources)
        return os.linesep.join(_str)


class Point(TaintBase):
    def __init__(self, raw):
        self.raw = raw
        self.raw_name, self.raw_cls = self.__parse_name_and_cls()
        self.name = None
        self.cls = None
        self.text = None
        self.behaviors = None
        self.is_skip = False

    def __parse_name_and_cls(self):
        if not self.raw:
            return "", ""
        elif "@" not in self.raw:
            return self.raw.strip(), self.raw.strip()
        else:
            return [piece.strip() for piece in self.raw.split("@")]

    def __str__(self):
        _str = list([])
        _str.append("raw_name=%s" % self.raw_name)
        _str.append("raw_cls=%s" % self.raw_cls)
        _str.append("name=%s" % self.name)
        _str.append("cls=%s" % self.cls)
        _str.append("behaviors=%s" % self.behaviors)
        if self.behaviors:
            _str.append("behaviors.pairs=%s" % self.behaviors.pairs)
            _str.append("behaviors.actions=%s" % self.behaviors.actions)
            _str.append("behaviors.resources=%s" % self.behaviors.resources)
        return os.linesep.join(_str)


class Flow(TaintBase):
    def __init__(self, raw_flow=None):
        self.raw = raw_flow
        self.source = None
        self.sink = None
        self.flow = None

        if self.raw:
            self.source, self.sink = self._parse_source_and_sink()

    def _parse_source_and_sink(self):
        source, sink = [piece.strip() for piece in self.raw.split("=>")]
        return Point(source), Point(sink)

    def parse(self, raw):
        self.raw = raw
        self.source, self.sink = self._parse_source_and_sink()
        return self


class Group(TaintBase):
    def __init__(self, flow=None, flow_text=None, related_text=None,
                 app_description=None, layout_strings=None, label=None,
                 filename=None):
        self.flow = Flow(flow)
        self.flow_text = Text(flow_text)
        self.related_text = Text(related_text)
        self.app_description = Text(app_description)
        self.layout_strings = Text(layout_strings)
        self.label = Label.parse(label if label else "")
        self.filename = filename if filename else ""

        self.__check_skip()
        self.prediction = None

    def parse_json(self, json_dict):
        """Parse from Json dict"""
        self.flow = Flow(json_dict.get("flow"))
        self.flow_text = Text("".join(json_dict.get("flow_text")))
        self.related_text = Text("".join(json_dict.get("related_text")))
        self.app_description = Text("".join(json_dict.get("app_description")))
        self.layout_strings = Text("".join(json_dict.get("layout_strings")))
        self.filename = str(json_dict.get("file", ""))
        self.label = Label.parse(json_dict.get("label", ""))

        self.__check_skip()

        return self

    def __check_skip(self):
        if self.app_description.raw:
            self.layout_strings.is_skip = True

    def __attrs(self):
        attrs = dict()
        attrs["flow"] = self.flow.raw
        attrs["flow_text"] = self.flow_text.raw
        attrs["related_text"] = self.related_text.raw
        attrs["app_description"] = self.app_description.raw
        attrs["layout_strings"] = self.layout_strings.raw
        attrs["filename"] = self.filename
        attrs["label"] = str(self.label)
        return attrs

    def __str__(self):
        return str(self.__attrs())


class GroupLabel(Enum):
    MALICIOUS = 0
    BENIGN = 1
    UNKNOWN = 2


class Label(TaintBase):
    @staticmethod
    def parse(raw_label):
        """Parse from string and covert it into type GroupLabel"""
        if raw_label.strip() == "M":
            return GroupLabel.MALICIOUS
        elif raw_label.strip() == "B":
            return GroupLabel.BENIGN
        return GroupLabel.UNKNOWN

# class PointInfo(TaintBase):
#     def __init__(self, class_name, description, behaviors):
#         if type(behaviors) is not entity.bahavior.Behavior:
#             if behaviors is not None:
#                 raise TypeError("Type of argument behaviors must be Point "
#                                 "Behavior")
#         self.class_name = class_name
#         self.description = description
#         self.behaviors = behaviors if behaviors else entity.behavior.Behavior()

# if __name__ == '__main__':
#     t = Point("")

# if __name__ == '__main__':
#     print(Group())
#     import simplejson as json
