#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from gensim.models import KeyedVectors

logging.basicConfig()
model = KeyedVectors.load_word2vec_format("phraseEmbedding.txt")
model.save("embedding.dat")
