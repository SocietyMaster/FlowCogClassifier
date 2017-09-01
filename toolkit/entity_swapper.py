#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

index_label = ["1)", "2)", "3)", "4)", "5)", "6)", "7)", "8)", "9)", "10)",
               "(1)", "(2)", "(3)", "(4)", "(5)", "(6)", "(7)", "(8)", "(9)",
               "(10)",
               "1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.", "10.", ">",
               "a)", "b)", "c)", "d)", "e)", "f)", "g)", "h)", "i)", "g)", "k)",
               "l)", "m)", "n)", "o)", "p)", "q)", "r)", "s)", "t)", "u)", "v)",
               "w)", "x)", "y)", "z)",
               "(a)", "(b)", "(c)", "(d)", "(e)", "(f)", "(g)", "(h)", "(i)",
               "(g)", "(k)", "(l)", "(m)", "(n)",
               "(o)", "(p)", "(q)", "(r)", "(s)", "(t)", "(u)", "(v)", "(w)",
               "(x)", "(y)", "(z)",
               "A)", "B)", "C)", "D)", "E)", "F)", "G)", "H)", "I)", "G)", "K)",
               "L)", "M)", "N)", "O)", "P)", "Q)", "R)", "S)", "T)", "U)", "V)",
               "W)", "X)", "Y)", "Z)",
               "(A)", "(B)", "(C)", "(D)", "(E)", "(F)", "(G)", "(H)", "(I)",
               "(G)", "(K)", "(L)", "(M)", "(N)", "(O)", "(P)", "(Q)", "(R)",
               "(S)", "(T)", "(U)", "(V)", "(W)", "(X)", "(Y)", "(Z)"]


class FormattedEntitySwapper(object):
    @staticmethod
    def _swap_index_label(text):
        text = text.strip()
        for label in sorted(index_label, key=lambda x: len(x), reverse=True):
            text = re.sub(re.escape(label), "\n", text)
        return text

    @staticmethod
    def _swap_url(text):
        return re.sub(
            r'(?i)\b((?:[a-z][\w-]+:(?:/{1,3}'
            r'|[a-z0-9%])|www\d{0,3}[.]'
            r'|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+'
            r'|\(([^\s()<>]+'
            r'|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+'
            r'|(\([^\s()<>]+\)))*\)'
            r'|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))', 'url', text)

    @staticmethod
    def _swap_email_address(text):
        return re.sub(r"\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*",
                      "email address", text)

    @staticmethod
    def _swap_br_tag(text):
        return re.sub(r"<br />|<br>", '\n', text)

    def swap(self, text):
        swap_pipeline = [self._swap_url, self._swap_email_address,
                         self._swap_br_tag, self._swap_index_label]
        for swap_function in swap_pipeline:
            text = swap_function(text)

        return text.strip()


class NamedEntitySwapper(object):
    def swap_sentences(self, sentences):
        sentences = [self.swap(sentence) for sentence in sentences]
        return sentences

    @staticmethod
    def swap(text):
        """
        Swap named entity with its label. Argument flow_text should be a single 
        sentence.
        :param text: A single sentence. Multiple sentences will lead 
        mis-recognition. 
        :return: Swapped flow_text.
        """
        iterators = re.finditer(r"[a-zA-Z]+", text)
        tmp = text
        pieces = []
        last_end = 0
        for i in iterators:
            start, end = i.span()
            pieces.append((tmp[last_end:start], False))
            pieces.append((tmp[start:end], True))
            last_end = end
        pieces.append((tmp[last_end:], False))
        words_to_pieces_dict = {}
        words = []
        words_cnt = 0
        for i, (piece, flag) in enumerate(pieces):
            if flag:
                words.append(piece)
                words_to_pieces_dict[words_cnt] = i
                words_cnt += 1

        all_pieces = [piece for piece, flag in pieces]
        return "".join(all_pieces)

# if __name__ == '__main__':
#     import os
#     swapper = NamedEntitySwapper()
#     flow_text = "Powered by Appsmelon." + os.linesep + "Powered by Appsmelon."
#     print swapper.swap(flow_text)
