#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

import configs
import stanford_corenlp


class TestCoreNLP(unittest.TestCase):
    def setUp(self):
        path = configs.Values.stanford_corenlp_dir
        self.corenlp = stanford_corenlp.StanfordCoreNLPWrapper(classpath=path)

    def test_parse(self):
        result = self.corenlp.parse(
            "Recognizes the true case of tokens in text where this information was lost, e.g., all upper case text. This is implemented with a discriminative model implemented using a CRF sequence tagger.")
        # print(result)


if __name__ == '__main__':
    unittest.main()
