"""Tokenizer"""

class Tokenizer(object):
    """Tokenizer class.

    Parameters:
        return_set (boolean): an attribute which is a flag to indicate whether to return a set of
                              tokens instead of a bag of tokens (defaults to False).
    """
    def __init__(self, return_set=False):
        self.return_set = return_set

    def get_return_set(self):
        """Get the return_set flag.

        Returns:
            The boolean value of the return_set attribute.
        """
        return self.return_set

    def set_return_set(self, return_set):
        """Set the return_set flag.

        Args:
            return_set (boolean): flag to indicate whether to return a set of tokens or a bag of tokens. 
        """
        self.return_set = return_set
        return True
