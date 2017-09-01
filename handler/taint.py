#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

import simplejson as json

import processer.scene
import toolkit.language_filter
import toolkit.tokenizer
from exception.handler import LackEnglishTextError
from handler.base import BaseHandler


class RawGroupsHandler(BaseHandler):
    @staticmethod
    def process(tainted_groups):
        logger = logging.getLogger(__name__)
        groups = tainted_groups
        groups = RawGroupsHandler.clean_duplicated(groups)
        formatted_groups = list()
        logger.debug("[Raw Text] Start to preprocess raw text")

        groups_length = len(groups)
        print_interval = 0.05
        last_print = print_interval

        for i, group in enumerate(groups):
            formatted_group = _RawGroupHandler.process(group)
            formatted_groups.append(formatted_group)

            processed_percentage = float(i) / groups_length
            if processed_percentage >= last_print:
                logger.debug(
                    "[Raw Text] processed:{percentage:.2f}%({i}/{len})".format(
                        percentage=100 * (float(i) / groups_length), i=i,
                        len=groups_length))
                last_print += print_interval
        return formatted_groups

    @staticmethod
    def clean_duplicated(tainted_groups):
        tainted_groups = list(set(tainted_groups))
        return tainted_groups


class _RawGroupHandler(BaseHandler):
    @staticmethod
    def process(tainted_group):
        logger = logging.getLogger(__name__)
        text_handler = RawTextHandler()
        point_handler = RawPointHandler()

        tainted_texts = [tainted_group.flow_text,
                         tainted_group.related_text,
                         tainted_group.app_description,
                         tainted_group.layout_strings]

        content_flag = False
        for i in range(len(tainted_texts)):
            if tainted_texts[i].is_skip:
                continue
            tainted_texts[i] = text_handler.process(tainted_texts[i])
            content_flag = content_flag or (
                tainted_texts[i].text is not None)
        if not content_flag:
            logger.error(LackEnglishTextError(
                "Not enough text found in give text"))
            for i in range(len(tainted_texts)):
                if (not tainted_texts[i].text) and (
                        not tainted_texts[i].is_skip):
                    tainted_texts[i].is_skip = True

        tainted_points = [tainted_group.flow.source, tainted_group.flow.sink]
        for i in range(len(tainted_points)):
            tainted_points[i] = point_handler.process(
                tainted_points[i])

        return tainted_group


class RawTextHandler(BaseHandler):
    @staticmethod
    def process(tainted_text):
        logger = logging.getLogger(__name__)
        if not tainted_text.raw:
            tainted_text.is_skip = True
            return tainted_text
        language_filter = toolkit.language_filter.LanguageFilter()
        en_chars_elements = language_filter.parse_english_chars(
            tainted_text.raw)
        en_chars = ("".join(en_chars_elements)).strip()
        if not en_chars:
            logger.warning("Not enough English text find in \"%s\"" % (
                tainted_text.raw))
            tainted_text.is_skip = True
            return tainted_text
        # print(en_chars)
        # en_chars = "\n".join(list(set([s.strip() for s in en_chars.split()])))
        tokenizer = toolkit.tokenizer.SentenceTokenizer()
        formatted_text = list()
        parse_trees = list()
        parsed_infos = list()
        # logger.debug("[Processing] text:{text}".format(text=en_chars))
        for sentences in tokenizer.token(en_chars.lower()):
            sentences = sentences.strip()
            # logger.debug("[Processing] split text:{text}".format(
            #     text=sentences))
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
            parsed_infos.append(parsed_info)
            text = sentences
            end_pos = 0
            for sentence in parsed_info:
                words = sentence["words"]
                for word_attr_tuple in words:
                    word = word_attr_tuple[0]
                    attr = word_attr_tuple[1]
                    begin_pos = int(attr["CharacterOffsetBegin"])
                    formatted_text.append(text[end_pos:begin_pos])
                    end_pos = int(attr["CharacterOffsetEnd"])
                    if word != attr["Lemma"]:
                        if word.lower() == "-lrb-":
                            formatted_text.append("(")
                        if word.lower() == "-rrb-":
                            formatted_text.append(")")
                        else:
                            formatted_text.append(attr["Lemma"].strip())
                    else:
                        formatted_text.append(text[begin_pos:end_pos].strip())

                parse_tree = sentence["parse_tree"]
                parse_trees.append(parse_tree)

        tainted_text.parsed_info = parsed_infos
        formatted_text = " ".join([s.strip() for s in (
            " ".join(formatted_text)).split() if s.strip()])
        # logger.debug("[Formatted Text] {0}".format(formatted_text))
        # logger.debug(parse_trees)
        tainted_text.text = formatted_text
        tainted_text.parse_trees = parse_trees

        return tainted_text


class RawPointHandler(BaseHandler):
    @staticmethod
    def process(tainted_point):
        logger = logging.getLogger(__name__)
        # tainted_point.name = processer.scene.Scene().whitespace_inserter.insert(
        #     tainted_point.raw_name.lower())
        tainted_point.name = tainted_point.raw_name.lower()
        tainted_point.cls = tainted_point.raw_cls
        sentence_tokenizer = toolkit.tokenizer.SentenceTokenizer()
        text = "\n".join(sentence_tokenizer.token(
            tainted_point.name + "\n" + tainted_point.cls))
        # logger.debug("[Point Text] {text}".format(text=text))
        tainted_point.text = text
        return tainted_point
