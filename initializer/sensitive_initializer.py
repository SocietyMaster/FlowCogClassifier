#!/usr/bin/env python
# -*- coding: utf-8 -*-
import simplejson
from scene import Scene

from configs.common import Values
from handler.behavior import BehaviorHandler

permissions_json_path = Values.permissions_json_path
with open(permissions_json_path, "r") as json_input:
    permissions_json = simplejson.load(json_input)
permissions_list_path = Values.permissions_list_path
with open(permissions_list_path, "r") as list_input:
    permissions_list = list_input.readlines()

permissions = list(permissions_json.keys()) + list(permissions_list)
permissions = [permission.strip() for permission in permissions if (
    permission.strip())]
permissions = list(set([permission[permission.rfind(".") + 1:].replace(
    "_", " ").lower() for permission in permissions]))
behaviors_handler = BehaviorHandler()
behaviors = []
for i in permissions:
    behaviors.append(behaviors_handler.process(i))

sensitive_words = []
for i in behaviors:
    sensitive_words += i.actions
    sensitive_words += i.resources
    for pair in i.pairs:
        sensitive_words.append(pair.action + " " + pair.resource)

for i in sensitive_words:
    print i

sensitive_content_path = Values.sensitive_content
with open(sensitive_content_path, "w") as output_file:
    for i in sensitive_words:
        output_file.write(i + "\n")

Scene().server.stop()
