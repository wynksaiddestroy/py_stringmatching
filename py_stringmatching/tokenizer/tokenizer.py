class Tokenizer(object):
    """Tokenizer class.

    Args:
        return_set (boolean): A flag to indicate whether to return a set of
                              tokens instead of a bag of tokens (defaults to False). 
                              
    Attributes: 
        return_set (boolean): An attribute to store the flag return_set. 
    """
    
    def __init__(self, return_set=False):
        self.return_set = return_set

    def get_return_set(self):
        """Get the value of the return_set flag.

        Returns:
            The boolean value of the return_set flag. 
        """
        return self.return_set

    def set_return_set(self, return_set):
        """Set the value of the return_set flag.

        Args:
            return_set (boolean): a flag to indicate whether to return a set of tokens instead of a bag of tokens.
        """
        self.return_set = return_set
        return True
