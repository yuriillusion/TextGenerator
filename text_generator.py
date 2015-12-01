import corpus
import random
import time
import logging
import sys

REGEX = r"[mMdD][rs]s?\. ?[\w,]+|[\w]+'?[\w,]+|[\.!\?:]"


class TextGenerator(object):
    def __init__(self, corpus):
        self.statements = corpus.statements.copy()
        self.BEGIN_CHAR = corpus.BEGIN_CHAR

    def next_token(self, token0, token1):
        extensions = self.statements[token0, token1]
        variants = sum(extensions.values())
        choice = random.randint(1, variants)
        for extension in extensions:
            if choice <= extensions[extension]:
                return extension
            else:
                choice -= extensions[extension]

    def gen_sentence(self):
        sentence = ''
        token0, token1 = self.BEGIN_CHAR, self.BEGIN_CHAR
        while True:
            token0, token1 = token1, self.next_token(token0, token1)
            if token1 == self.BEGIN_CHAR:
                break
            elif token1 in '.!?,;:' or token0 == self.BEGIN_CHAR:
                sentence += token1
            else:
                sentence += ' ' + token1
        return sentence.capitalize()

    def gen_text_line(self, sentences_count, min_paragraph_size,
                      max_paragraph_size):
        try:
            if min_paragraph_size < 0 or max_paragraph_size < 0 or\
                            max_paragraph_size < min_paragraph_size or\
                            sentences_count < 0:
                raise ValueError()
            paragraph_size = random.randint(min_paragraph_size,
                                            max_paragraph_size)
            yield '\t'
            for sentence_number in xrange(sentences_count):
                paragraph_size -= 1
                if paragraph_size:
                    ending = ' '
                else:
                    ending = '\n\t'
                    paragraph_size = random.randint(min_paragraph_size,
                                                    max_paragraph_size)
                yield self.gen_sentence() + ending
        except ValueError:
            print 'Bad Values of Arguments.'


if __name__ == "__main__":
    logging.basicConfig(format='%(message)s', level=logging.INFO)
    template = '{:-^50}'

    REGEX = r"[mMdD][rs]s?\. ?[\w,]+|[\w]+'?[\w,]+|[\.!\?:]"
    END_CHARS = '.?!'
    corpus = corpus.Corpus(REGEX, END_CHARS)

    INPUT_FILE_NAME = sys.argv[1]
    log = 'Reading from {}'.format(INPUT_FILE_NAME)
    logging.info(template.format(log))
    start_time = time.time()

    corpus.load(INPUT_FILE_NAME)

    log = 'Time: {} s'.format(time.time() - start_time)
    logging.info(template.format(log))

    OUTPUT_FILE_NAME = sys.argv[2]
    SENTENCES_COUNT = int(sys.argv[3])
    log = 'Writing to {}'.format(OUTPUT_FILE_NAME)
    logging.info(template.format(log))
    start_time = time.time()

    text_generator = TextGenerator(corpus)
    with open(OUTPUT_FILE_NAME, 'w') as f:
        f.writelines(text_generator.gen_text_line(SENTENCES_COUNT, 1, 10))

    log = 'Time: {} s'.format(time.time() - start_time)
    logging.info(template.format(log))

