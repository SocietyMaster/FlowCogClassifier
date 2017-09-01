#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

import langid

from coding_transformer import CodingTransformer


class LanguageFilter(object):
    def __init__(self):
        self._identifier = langid.langid.LanguageIdentifier.from_modelstring(
            langid.langid.model, norm_probs=True)
        self.en_chars_range_list = [
            range(0x0000, 0x007f),  # C0 Controls and Basic Latin
            range(0x0080, 0x00ff),  # C1 Controls and Latin-1 Supplement
            range(0x0100, 0x017f),  # Latin Extended-A
            range(0x0180, 0x024f),  # Latin Extended-B
            range(0x0250, 0x02af),  # IPA Extension
            range(0x02b0, 0x02ff),  # Spacing Modifier Letters
        ]

        # Need to add english unicode punctuation characters set with Chinese
        #  unicode characters set to ensure the integrity of Chinese sentences.

        # self.punctuations_range_list = [
        #     range(0x2000, 0x206f),  # General_punctuation
        # ]
        # self.zh_chars_range_list = [
        #     range(0x3400, 0x4db5),  # CJK Unified Ideographs Extension A 3.0
        #     range(0x4e00, 0x9fa5),  # CJK Unified Ideographs 1.1
        #     range(0x9fa6, 0x9fbb),  # CJK Unified Ideographs 4.1
        #     range(0xf900, 0xfa2d),  # CJK Unified Ideographs 1.1
        #     range(0xfa30, 0xfa6a),  # CJK Unified Ideographs 3.2
        #     range(0xfa70, 0xfad9),  # CJK Unified Ideographs 4.1
        #     range(0x20000, 0x2a6d6),  # CJK Unified Ideographs Extension 3.1
        #     range(0x2f800, 0x2fa1d),  # CJK Compatibility Supplement 3.1
        #     range(0xff00, 0xffef),  # Half-width and Full-width forms
        #     range(0x2e80, 0x2ef3),  # CJK Radicals Supplement
        #     range(0x3000, 0x303f),  # CJK Symbols and Punctuation
        #     range(0x31c0, 0x31e3),  # CJK Strokes
        # ]

    def parse_english_chars(self, text):
        text = CodingTransformer.decode(text)
        regular_expression = "[" + "|".join(
            [unichr(range_field[0]) + "-" + unichr(range_field[len(
                range_field) - 1]) for range_field in (
                 self.en_chars_range_list)]) + "]+"
        return re.findall(regular_expression, text)

    # def _parse_chinese(self, flow_text):
    #     flow_text = self._decode(flow_text)
    #     regular_expression = "[" + "|".join(
    #         [unichr(0x20)] + [unichr(range_field[0]) + "-" + unichr(
    #             range_field[len(range_field) - 1]) for range_field in(
    #              self.zh_chars_range_list)]) + "]+"
    #     return re.findall(regular_expression, flow_text)

    def _filter_en(self, text):
        en_texts = self.parse_english_chars(text)
        filtered_text = []
        for text in en_texts:
            lang, prob = self._identifier.classify(text.lower())
            if lang == "en":
                filtered_text.append(text)
        return filtered_text

    # lang_set is left for further multilingual extension
    def filter(self, text, lang_set=None):
        return self._filter_en(text)


if __name__ == '__main__':
    print(LanguageFilter().filter("let me tell you测试Guten Tag"))
