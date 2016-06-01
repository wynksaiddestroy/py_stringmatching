"""Delimiter based tokenizer"""

import re

from py_stringmatching import utils
from py_stringmatching.tokenizer.tokenizer import Tokenizer


class DelimiterTokenizer(Tokenizer):
    """Delimiter tokenizer class.

    Parameters:
        delim_set (set): set of delimiter strings (defaults to space delimiter)
        return_set (boolean): flag to indicate whether to return a set of
                              tokens. (defaults to False) 
    """
    def __init__(self, delim_set=set([' ']), return_set=False):
        if not isinstance(delim_set, set):
            delim_set = set(delim_set)
        self.__delim_set = delim_set
        self.__delim_regex = re.compile('|'.join(
            map(lambda delim : re.escape(delim), self.__delim_set)))
        super(DelimiterTokenizer, self).__init__(return_set)

    def tokenize(self, input_string):
        """
        Tokenizes input string based on the set of delimiters.

        Args:
            input_string (str): Input string

        Returns:
            Token list (list)

        Raises:
            TypeError : If the input is not a string

        Examples:
            >>> delim_tok = DelimiterTokenizer() 
            >>> delim_tok.tokenize('data science')
            ['data', 'science']
            >>> delim_tok = DelimiterTokenizer(['$#$']) 
            >>> delim_tok.tokenize('data$#$science')
            ['data', 'science']
            >>> delim_tok = DelimiterTokenizer([',', '.']) 
            >>> delim_tok.tokenize('data,science.data,integration.')
            ['data', 'science', 'data', 'integration']
            >>> delim_tok = DelimiterTokenizer([',', '.'], return_set=True) 
            >>> delim_tok.tokenize('data,science.data,integration.')
            ['data', 'science', 'integration']

        """
        utils.tok_check_for_none(input_string)
        utils.tok_check_for_string_input(input_string)
    
        token_list = list(filter(None, self.__delim_regex.split(input_string)))

        if self.return_set:
            return utils.convert_bag_to_set(token_list)

        return token_list
