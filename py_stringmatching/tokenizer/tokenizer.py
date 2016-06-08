"""Tokenizer"""

class Tokenizer(object):
    """Tokenizer class.

    Parameters:
        return_set (boolean): flag to indicate whether to return a set of
                              tokens. (defaults to False) 
    """
    def __init__(self, return_set=False):
        self.return_set = return_set

    def get_return_set(self):
        """
        Get the return_set flag

        Returns:
            return_set (boolean)
        """
        return self.return_set

    def set_return_set(self, return_set):
        """
        Set the return_set flag

        Args:
            return_set (boolean): flag to indicate whether to return a set of tokens. 
        """
        self.return_set = return_set
        return True
