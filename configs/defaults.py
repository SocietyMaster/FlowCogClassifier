#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

# Constant environment related value
SOURCE_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
PROJECT_ROOT = os.path.dirname(SOURCE_ROOT)
DATA_ROOT = os.path.join(PROJECT_ROOT, "data")
LOG_ROOT = os.path.join(PROJECT_ROOT, "log")
