import re
import os
import json
import time
import logging
import sys
from collections import defaultdict, Counter


class Corpus(object):
    BEGIN_CHAR = '%'
    AUX_DELIMITER = '#'

    def __init__(self, regex, end_chars):
        self.MATCHER = re.compile(regex)
        self.END_CHARS = end_chars
        self.statements = defaultdict(Counter)

    def read_from_dir(self, input_dir_name):
        self.statements.clear()
        for root, dirs, files in os.walk(input_dir_name):
            for file in files:
                self.upgrade(os.path.join(root, file))

    def dump(self, output_file_name):
        with open(output_file_name, 'w') as f:
            delim = Corpus.AUX_DELIMITER
            statements_for_dumping = {delim.join(k): v for k, v in
                                      self.statements.iteritems()}
            json.dump(statements_for_dumping, f)

    def load(self, input_file_name):
        with open(input_file_name, 'r') as f:
            dumped_statements = json.load(f)
            delim = Corpus.AUX_DELIMITER
            self.statements = {tuple(k.split(delim)): v for k, v in
                               dumped_statements.iteritems()}

    def upgrade(self, input_file_name):
        with open(input_file_name, 'r') as f:
            lines = Corpus.__gen_lines__(f)
            tokens = self.__gen_tokens__(lines)
            triples = self.__gen_triplets__(tokens)
            for token0, token1, token2 in triples:
                self.statements[token0, token1][token2] += 1

    @staticmethod
    def __gen_lines__(file):
        for line in file:
            yield line.lower()

    def __gen_tokens__(self, lines):
        for line in lines:
            for token in self.MATCHER.findall(line):
                yield token

    def __gen_triplets__(self, tokens):
        token0, token1 = Corpus.BEGIN_CHAR, Corpus.BEGIN_CHAR
        for token2 in tokens:
            yield token0, token1, token2
            if token2 in self.END_CHARS:
                yield token1, token2, Corpus.BEGIN_CHAR
                yield token2, Corpus.BEGIN_CHAR, Corpus.BEGIN_CHAR
                token0, token1 = Corpus.BEGIN_CHAR, Corpus.BEGIN_CHAR
            else:
                token0, token1 = token1, token2

if __name__ == '__main__':
    logging.basicConfig(format='%(message)s', level=logging.INFO)
    template = '{:-^50}'

    REGEX = r"[mMdD][rs]s?\. ?[\w,]+|[\w]+'?[\w,]+|[\.!\?:]"
    END_CHARS = '.?!'
    corpus = Corpus(REGEX, END_CHARS)

    INPUT_FILE_NAME = sys.argv[1]
    log = 'Reading from {}'.format(INPUT_FILE_NAME)
    logging.info(template.format(log))
    start_time = time.time()

    corpus.read_from_dir(INPUT_FILE_NAME)

    log = 'Time: {} s'.format(time.time() - start_time)
    logging.info(template.format(log))

    DUMP_FILE_NAME = sys.argv[2]
    log = 'Dumping in {}'.format(DUMP_FILE_NAME)
    logging.info(template.format(log))
    start_time = time.time()

    corpus.dump(DUMP_FILE_NAME)

    log = 'Time: {} s'.format(time.time() - start_time)
    logging.info(template.format(log))
