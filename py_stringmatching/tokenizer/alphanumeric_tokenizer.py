"""Alphanumeric tokenizer"""

import re

from py_stringmatching import utils
from py_stringmatching.tokenizer.definition_tokenizer import DefinitionTokenizer


class AlphanumericTokenizer(DefinitionTokenizer):
    """Alphanumeric tokenizer class.

    Parameters:
        return_set (boolean): flag to indicate whether to return a set of
                              tokens. (defaults to False) 
    """
    def __init__(self, return_set=False):
        self.__alnum_regex = re.compile('[a-zA-Z0-9]+')
        super(AlphanumericTokenizer, self).__init__(return_set)

    def tokenize(self, input_string):
        """
        Tokenizes input string into alphanumeric tokens.

        An alphanumeric token is defined as consecutive sequence of alphanumeric characters.

        Args:
            input_string (str): Input string

        Returns:
            Token list (list)

        Raises:
            TypeError : If the input is not a string

        Examples:
            >>> alnum_tok = AlphanumericTokenizer()
            >>> alnum_tok.tokenize('data9,(science), data9#.(integration).88')
            ['data9', 'science', 'data9', 'integration', '88']
            >>> alnum_tok.tokenize('#.&')
            []
            >>> alnum_tok = AlphanumericTokenizer(return_set=True) 
            >>> alnum_tok.tokenize('data9,(science), data9#.(integration).88')
            ['data9', 'science', 'integration', '88']
                      
        """
        utils.tok_check_for_none(input_string)
        utils.tok_check_for_string_input(input_string)

        token_list = list(filter(None,
                                 self.__alnum_regex.findall(input_string)))

        if self.return_set:
            return utils.convert_bag_to_set(token_list)

        return token_list
