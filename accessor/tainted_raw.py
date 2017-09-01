#!/usr/bin/env python
# -*- coding: utf-8 -*-
import accessor.loader


class TaintedRawLoader(object):
    @staticmethod
    def get_raw_tainted_groups(path):
        raw = accessor.loader.JsonLoader.load(path)
        return raw

    @staticmethod
    def get_tainted_class_info(path):
        return accessor.loader.JsonLoader.load(path)

    @staticmethod
    def get_sources_sinks(path):
        with open(path, "r") as input_file:
            lines = input_file.readlines()

        entries = [line.strip() for line in lines if line.strip() and (
            not line.startswith("%"))]

        class_names = set()
        for entry in entries:
            class_name = entry[1:].split(":")[0]
            class_names.add(class_name)

        return list(class_names)

# if __name__ == '__main__':
#     from accessor.scene import Scene
#     path = Scene().config.get("resources", "tainted_class_info_path")
#     tainted_class_info_path = get_tainted_class_json(path)
