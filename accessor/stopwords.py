#!/usr/bin/env python
# -*- coding: utf-8 -*-
import nltk.corpus


def get_stopwords(path):
    with open(path, "r") as manual_input:
        manual_sw = manual_input.readlines()
    stopwords = nltk.corpus.stopwords.words("english")
    manual_sw = [word.strip() for word in manual_sw]
    sw = list(set(stopwords + manual_sw))
    return sw
