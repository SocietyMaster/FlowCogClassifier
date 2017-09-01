#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

import processer.scene
import toolkit.entity_swapper
import toolkit.whitespace_inserter


class SentenceTokenizer(object):
    def __init__(self):
        self._formatted_entity_swapper = (
            toolkit.entity_swapper.FormattedEntitySwapper())
        self._named_entity_swapper = toolkit.entity_swapper.NamedEntitySwapper()
        self._whitespace_inserter = processer.scene.Scene().whitespace_inserter

    @staticmethod
    def _sentences_splitter(text):
        return re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=.|\?|!)(\s|(?=["
                        r"A-Z]))", text)

    @staticmethod
    def _punctuation_trimmer(text):
        return re.sub(r"[^A-Za-z0-9.,?!:]+", " ", text)

    @staticmethod
    def _strict_punctuation_trimmer(text):
        return re.sub(r"[^A-Za-z]+", " ", text)

    def token(self, raw_text):
        raw_paragraphs = raw_text.strip().split("\n")
        sentences = []
        for raw_paragraph in raw_paragraphs:
            paragraph = self._formatted_entity_swapper.swap(raw_paragraph)
            raw_sentences = paragraph.split("\n")
            trimmed_sentences = [self._punctuation_trimmer(sentence) for
                                 raw_sentence in raw_sentences for sentence
                                 in self._sentences_splitter(raw_sentence)]
            trimmed_sentences = "\n".join(trimmed_sentences).split(
                ".|,|?|!|:|\n")

            trimmed_sentences = [self._strict_punctuation_trimmer(
                sentence.strip()) for sentence in trimmed_sentences]

            sentences += [self._whitespace_inserter.insert_with_sentence(
                sentence.strip()) for sentence in trimmed_sentences
                if sentence.strip()]
        return sentences
