from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import time

import accessor.sensitive_content
import accessor.stopwords
import accessor.tainted_raw
import configs
import model.embedding_model
import model.similarity_model
import stanford_corenlp.wrapper
import toolkit.language_filter
import toolkit.whitespace_inserter
from pattern.singleton import Singleton


class Scene(object):
    """
    To preload large modules and persist in memory.
    """
    __metaclass__ = Singleton

    def __init__(self):
        logger = logging.getLogger()

        logger.info("[Scene] First time to load scene, initializing...")
        logger.info("[Loading] loading components...")

        logger.info("[Loading] whitespace inserter...")
        sorted_words_path = configs.Values.sorted_words
        self.whitespace_inserter = (
            toolkit.whitespace_inserter.WhitespaceInserter(sorted_words_path))
        logger.info("[Finished] Whitespace inserter loaded.")

        logger.info("[Loading] loading corpus resources...")
        # self.tainted_class_info = (
        #     accessor.tainted_raw.TaintedRawLoader.get_tainted_class_info(
        #         configs.Values.tainted_class_info_path))
        sensitive_content_path = configs.Values.sensitive_content
        self.sensitive_content = (
            accessor.sensitive_content.get_sensitive_contents(
                sensitive_content_path))
        logger.info("[Finished] Corpus resources loaded.")

        similarity_handler_stopwords_path = configs.Values.stopwords_path
        self.similarity_handler_stopwords = accessor.stopwords.get_stopwords(
            similarity_handler_stopwords_path)

        logger.info("[Loading] loading model...")
        embedding_model_path = configs.Values.word2vec_model_path
        self.embedding_model = model.embedding_model.EmbeddingModel(
            embedding_model_path)
        logger.info("[Finished] Model loaded.")

        logger.info("[Loading] loading Stanford Core NLP Parser...")
        self.stanford_nlp_parser = (
            stanford_corenlp.wrapper.StanfordCoreNLPWrapper(
                configs.Values.stanford_corenlp_dir))
        logger.info("[Finished] Stanford Core NLP Parser loaded.")
        logger.info("[Finished] all components loaded.")

    def restart_stanford_nlp_parser(self):
        logger = logging.getLogger(__name__)
        logger.info("[Restart] Restart Stanford Core NLP Parser.")
        del self.stanford_nlp_parser
        time.sleep(10)
        self.stanford_nlp_parser = (
            stanford_corenlp.wrapper.StanfordCoreNLPWrapper(
                configs.Values.stanford_corenlp_dir))
