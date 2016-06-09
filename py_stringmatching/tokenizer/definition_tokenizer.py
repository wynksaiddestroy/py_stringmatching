"""Definition based tokenizer"""

from py_stringmatching.tokenizer.tokenizer import Tokenizer


class DefinitionTokenizer(Tokenizer):
    """A class of tokenizers that uses a definition (e.g., alphabetical, alphanumeric, qgram) to find tokens, as opposed to using delimiters (e.g., whitespace). 

    Parameters:
        return_set (boolean): An attribute which is a flag to indicate whether to return a set of
                              tokens instead of a bag of tokens (defaults to False).
    """
    def __init__(self, return_set=False):
        super(DefinitionTokenizer, self).__init__(return_set)
