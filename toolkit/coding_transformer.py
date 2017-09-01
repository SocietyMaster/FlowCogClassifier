#!/usr/bin/env python
# -*- coding: utf-8 -*-


class CodingTransformer(object):
    @staticmethod
    def decode(text):
        """
        Transform coding of string from utf-8 to ASCII.
        :param text: Raw input flow_text.
        :return: String with ASCII coding.
        """
        try:
            return text.decode("utf-8")
        except (UnicodeDecodeError, UnicodeEncodeError):
            return text
        except Exception:
            raise

    @staticmethod
    def encode(text):
        """
        Transform coding of string from ASCII to utf-8.
        :param text: Raw input flow_text.
        :return: String with utf-8 coding.
        """
        try:
            text.encode("utf-8")
        except (UnicodeDecodeError, UnicodeEncodeError):
            return text
        except Exception:
            raise
