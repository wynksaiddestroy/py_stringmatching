"""Tokenizer"""

class Tokenizer(object):
    """Tokenizer class.

    Parameters:
        return_set (boolean): flag to indicate whether to return a set of
                              tokens. (defaults to False) 
    """
    def __init__(self, return_set=False):
        self.return_set = return_set
