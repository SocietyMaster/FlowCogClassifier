#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Behavior(object):
    def __init__(self, pairs=None, actions=None, resources=None):
        self.pairs = list(pairs) if pairs else []
        self.actions = list(actions) if actions else []
        self.resources = list(resources) if resources else []

    def __add__(self, other):
        pairs = set(self.pairs + list(other.pairs))
        actions = set(self.actions + list(other.actions))
        resources = set(self.resources + list(other.resources))
        return Behavior(pairs=pairs, actions=actions, resources=resources)

    def __str__(self):
        return str({"pairs": self.pairs, "actions": self.actions,
                    "resources": self.resources})

# class BehaviorPair(object):
#     def __init__(self, action, resource):
#         self.action = action
#         self.resource = resource
#
#     def __str__(self):
#         return "{action} {resource}".format(
#             action=self.action, resource=self.resource)
#
#     def __repr__(self):
#         return self.__str__()
#
#     def __eq__(self, other):
#         if isinstance(other, BehaviorPair):
#             return (self.action + " " + self.resource) == (
#                 other.action + " " + other.resource)
#         else:
#             return False
#
#     def __hash__(self):
#         return hash(self.__repr__())
