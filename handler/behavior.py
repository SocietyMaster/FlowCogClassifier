#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import string

import nltk.corpus
import nltk.tree
import simplejson as json

import entity.behavior
import processer.scene
import toolkit.tokenizer
from handler.base import BaseHandler


class BehaviorHandler(BaseHandler):
    @staticmethod
    def _parse_behaviors(tree):
        stopwords = nltk.corpus.stopwords.words("english") + (
            ["-LRB-", "-RRB-"]) + list(string.punctuation)
        leaf_pos = tree.treepositions("leaves")

        nn_pos = [pos for pos in leaf_pos if "NN" in (
            tree[pos[:len(pos) - 1]].label()) and tree[pos] not in stopwords]
        vb_pos = [pos for pos in leaf_pos if "VB" in (
            tree[pos[:len(pos) - 1]].label()) and tree[pos] not in stopwords]

        resources = set([tree[pos] for pos in nn_pos])
        actions = set([tree[pos] for pos in vb_pos])

        nn_seq = ["".join(map(str, pos)) for pos in nn_pos]
        vb_seq = ["".join(map(str, pos)) for pos in vb_pos]
        vp_seq = []
        np_seq = []
        noun_phrases = {}
        for pos in tree.treepositions():
            if pos in leaf_pos:
                continue
            if "VP" in tree[pos].label():
                vp_seq.append("".join(map(str, pos)))
            if "NP" in tree[pos].label():
                np_seq.append("".join(map(str, pos)))
                pos_tagged_wrods = tree[pos].pos()
                if len(pos_tagged_wrods) < 2:
                    continue
                for i in range(len(pos_tagged_wrods)):
                    if i >= len(pos_tagged_wrods) - 1:
                        continue
                    if ("NN" or "PRP") in pos_tagged_wrods[i][1] and "NN" in (
                            pos_tagged_wrods[i + 1][1]):
                        noun_phrase = pos_tagged_wrods[i][0] + "_" + (
                            pos_tagged_wrods[i + 1][0])
                        noun_phrases[noun_phrase] = "".join(map(str, pos))

        behavior_pairs = []
        # bi-gram verb + noun
        for i, nn in enumerate(nn_seq):
            for j, vb in enumerate(vb_seq):
                prefix = get_common_prefix(nn, vb)
                if prefix in vp_seq:
                    noun = tree[nn_pos[i]]
                    verb = tree[vb_pos[j]]
                    behavior_pairs.append(verb + " " + noun)

        # tri-gram verb + phrase
        for phrase, pos in noun_phrases.items():
            for j, vb in enumerate(vb_seq):
                prefix = get_common_prefix(pos, vb)
                if prefix in vp_seq:
                    verb = tree[vb_pos[j]]
                    behavior_pairs.append(verb + " " + phrase)

        behavior_pairs_set = set([])
        for pair in set(behavior_pairs):
            action, resource = pair.split(" ")
            behavior_pairs_set.add(action + " " + resource.replace("_", " "))

        noun_phrase = list(set([p.replace("_", " ") for p in
                                noun_phrases.keys()]))

        resources = list(resources) + noun_phrase

        return entity.behavior.Behavior(
            pairs=behavior_pairs_set, actions=actions, resources=resources)

    @staticmethod
    def process(raw_text):
        logger = logging.getLogger(__name__)
        text = raw_text.lower()
        tokenizer = toolkit.tokenizer.SentenceTokenizer()
        parse_trees = list()
        for sentences in tokenizer.token(text):
            sentences = sentences.strip()
            if not sentences:
                continue
            try:
                parsed_result = processer.scene.Scene(
                ).stanford_nlp_parser.parse(sentences)
            except Exception as e:
                logger.error(e.message)
                processer.scene.Scene().restart_stanford_nlp_parser()
                continue
            parsed_json = json.loads(parsed_result)
            parsed_info = parsed_json["sentences"]
            for sentence in parsed_info:
                parse_tree = sentence["parse_tree"]
                parse_trees.append(parse_tree)
        behaviors = BehaviorHandler.parse(parse_trees)
        return behaviors

    @staticmethod
    def parse(parse_trees):
        dependencies = [nltk.tree.Tree.fromstring(parse_tree) for (
            parse_tree) in parse_trees]
        behaviors = list()
        for dependency in dependencies:
            behavior = BehaviorHandler._parse_behaviors(dependency)
            behaviors.append(behavior)
        if behaviors:
            return reduce(lambda x, y: x + y, behaviors)
        else:
            return entity.behavior.Behavior()


class GroupsBehaviorHandler(BaseHandler):
    @staticmethod
    def process(tainted_groups):
        logger = logging.getLogger(__name__)
        logger.debug("[Behavior] starts to extract behaviors")
        groups = tainted_groups
        processed_tainted_groups = []

        groups_length = len(groups)
        print_interval = 0.05
        last_print = print_interval

        for i, group in enumerate(groups):
            processed_tainted_groups.append(
                _GroupBehaviorHandler.process(group))

            processed_percentage = float(i) / groups_length
            if processed_percentage >= last_print:
                logger.debug(
                    "[Behavior] processed:{percentage:.2f}%({i}/{len})".format(
                        percentage=100 * (float(i) / groups_length), i=i,
                        len=groups_length))
                last_print += print_interval
        return processed_tainted_groups


class _GroupBehaviorHandler(BaseHandler):
    @staticmethod
    def process(tainted_group):
        logger = logging.getLogger(__name__)
        tainted_texts = [tainted_group.flow_text,
                         tainted_group.related_text,
                         tainted_group.app_description,
                         tainted_group.layout_strings]

        for i in range(len(tainted_texts)):
            if tainted_texts[i].is_skip:
                continue
            if tainted_texts[i].parse_trees:
                behaviors = BehaviorHandler.parse(tainted_texts[i].parse_trees)
            else:
                behaviors = BehaviorHandler.process(tainted_texts[i].text)
            # logger.debug("[Text Behaviors]: {behaviors}".format(
            #     behaviors=behaviors))
            tainted_texts[i].behaviors = behaviors

        tainted_points = [tainted_group.flow.source, tainted_group.flow.sink]
        for point in tainted_points:
            behaviors = BehaviorHandler.process(point.text)
            # logger.debug("[Point Behaviors]: {behaviors}".format(
            #     behaviors=behaviors))
            point.behaviors = behaviors

        return tainted_group


def get_common_prefix(str1, str2):
    min_len = min(len(str1), len(str2))
    for i in range(min_len):
        if str1[i] == str2[i]:
            continue
        else:
            return str1[:i]
    return str1[:min_len]
