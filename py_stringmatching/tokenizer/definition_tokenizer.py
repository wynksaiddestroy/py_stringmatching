"""Definition based tokenizer"""

from py_stringmatching.tokenizer.tokenizer import Tokenizer


class DefinitionTokenizer(Tokenizer):
    """Definition based tokenizer class.

    Attributes:
        return_set (boolean): flag to indicate whether to return a set of
                              tokens. (defaults to False) 
    """
    def __init__(self, return_set=False):
        super(DefinitionTokenizer, self).__init__(return_set)
