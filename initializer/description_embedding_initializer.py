#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3

from accessor.persist import Persister
from objects.tookit.language_filter import LanguageFilter

from configs.common import Values
from toolkit.tokenizer import SentenceTokenizer


def data_from_db():
    database_path = Values.database_path
    db_connection = sqlite3.connect(database_path)
    sql_query = "select packageName, description from metainfo"
    db_cursor = db_connection.execute(sql_query)
    db_data = []
    for row in db_cursor:
        package_name = row[0]
        description = row[1]
        if package_name and description:
            db_data.append({"package_name": package_name,
                            "description": description})
    return db_data


def decode_list(texts):
    print("starting to decode...")
    decoded_list = []
    for i, text in enumerate(texts):
        print("decoding %d/%d" % (i, len(texts)))
        try:
            dtext = text.encode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            dtext = text
        try:
            dtext = dtext.decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            dtext = ""
        decoded_list.append(dtext)
    return decoded_list


def _clean_text(text):
    language_filter = LanguageFilter()
    return "\n".join(language_filter.parse_english_chars(text))


def clean_characters(texts):
    print("cleaning irrelevant characters...")
    cleaned_text = []
    for i, text in enumerate(texts):
        print("cleaning %d/%d" % (i, len(texts)))
        cleaned_text = _clean_text(text)
    return cleaned_text


def sent_token(texts):
    print("tokenizing sentences...")
    sentence_tokenizer = SentenceTokenizer()
    tokened = []
    for i, text in enumerate(texts):
        print("tokenizing %d/%d" % (i, len(texts)))
        result = sentence_tokenizer.token(text)
        if result:
            tokened += result
    return tokened


def init():
    json_data_dump_path = Values.json_data_dump_path
    db_data = data_from_db()
    Persister.json_save(db_data, json_data_dump_path)
    descriptions = []
    for item in db_data:
        description = item["description"]
        descriptions.append(description)
    dsents = decode_list(descriptions)
    en_sents = clean_characters(dsents)
    all_text = "\n".join(en_sents)
    print("persisting intermediate cleaned text")
    with open("cleaned_char_sentes.txt", "w") as oc_file:
        oc_file.write(all_text)
    tokened_sents = sent_token(all_text.split("\n"))
    print("persisting intermediate cleaned text")
    all_text = "\n".join(tokened_sents)
    with open("tokened_sents.txt", "w") as os_file:
        os_file.write(all_text)


if __name__ == '__main__':
    init()
