#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import re


class WhitespaceInserter(object):
    def __init__(self, sorted_words_dictionary_path):
        with open(sorted_words_dictionary_path, "r") as input_file:
            words = input_file.read().split()

        self._words = words
        self._word_cost = dict([(word, math.log((i + 1) * math.log(len(
            words)))) for i, word in enumerate(words)])
        self._max_word_length = max([len(word) for word in words])

    @staticmethod
    def _project_space_to_original_text(inserted="", original=""):
        original_chars = list(original)
        inserted_chars = list(inserted)
        for i, c in enumerate(inserted_chars):
            if c == " " and original_chars[i] != " ":
                original_chars.insert(i, " ")
        return "".join(original_chars)

    def _insert(self, word):
        if len(word) < 4:
            return word

        def best_match(i):
            candidates = enumerate(
                reversed(cost[max(0, i - self._max_word_length):i]))
            return min((c + self._word_cost.get(word[i - k - 1:i], 9e999),
                        k + 1) for
                       k, c in candidates)

        cost = [0]
        for i in range(1, len(word) + 1):
            c, k = best_match(i)
            cost.append(c)
        out = []
        i = len(word)
        while i > 0:
            c, k = best_match(i)
            assert c == cost[i]
            out.append(word[i - k:i])
            i -= k

        max_substring_len = max([len(s) for s in out])
        if max_substring_len <= 1:
            return word

        return " ".join(reversed(out))

    def insert(self, word):
        lower_text = word.lower()
        return self._project_space_to_original_text(
            self._insert(lower_text), word)

    def _insert_with_sentence(self, sentence):
        word_finder = re.compile(r"[a-zA-z]+")
        word_iterators = word_finder.finditer(sentence)
        tmp = sentence
        pieces = []
        last_end = 0
        for i in word_iterators:
            start, end = i.span()
            pieces.append((tmp[last_end:start], False))
            pieces.append((tmp[start:end],
                           True if len(tmp[start:end]) > 3 else False))
            last_end = end
        pieces.append((tmp[last_end:], False))

        pieces = [self._insert(piece) if (flag and piece not in self._words)
                  else piece for piece, flag in pieces]
        return "".join(pieces)

    def insert_with_sentence(self, sentence):
        lower_sentence = sentence.lower()
        return self._project_space_to_original_text(
            self._insert_with_sentence(lower_sentence), sentence)

# if __name__ == '__main__':
#     from accessor.scene import Scene
# #     test = "Test wordSplit Whyhere. 00:00 is a best time.()()"
#     inserter = WhitespaceInserter(Scene().config.get("resources",
#                                                      "sorted_words"))
# #     print inserter.insert_with_sentence(test)
#     print inserter.insert("testFunction")
#
