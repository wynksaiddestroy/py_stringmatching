"""Definition based tokenizer"""

from py_stringmatching.tokenizer.tokenizer import Tokenizer


class DefinitionTokenizer(Tokenizer):
    """A class of tokenizers that uses a definition to find tokens, as opposed to using delimiters.
    
    Examples of definitions include alphabetical tokens, qgram tokens. Examples of delimiters include white space, punctuations.

    Parameters:
        return_set (boolean): An attribute which is a flag to indicate whether to return a set of
                              tokens instead of a bag of tokens (defaults to False).
    """
    def __init__(self, return_set=False):
        super(DefinitionTokenizer, self).__init__(return_set)
