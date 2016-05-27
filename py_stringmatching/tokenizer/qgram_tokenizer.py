"""Qgram based tokenizer"""

from py_stringmatching import utils
from py_stringmatching.compat import _range
from py_stringmatching.tokenizer.definition_tokenizer import DefinitionTokenizer


class QgramTokenizer(DefinitionTokenizer):
    """Qgram tokenizer class.

    Attributes:
        qval (int): Q-gram length (defaults to 2)
        return_set (boolean): flag to indicate whether to return a set of
                              tokens. (defaults to False) 
    """
    def __init__(self, qval=2, return_set=False):
        if qval < 1:
            raise AssertionError("qval cannot be less than 1") 
        self.qval = qval
        super(QgramTokenizer, self).__init__(return_set)

    def tokenize(self, input_string):
        """
        Tokenizes input string into q-grams.

        A q-gram is defined as all sequences of q characters. Q-grams are also known as n-grams and
        k-grams.

        Args:
            input_string (str): Input string

        Returns:
            Token list (list)

        Raises:
            TypeError : If the input is not a string

        Examples:
            >>> qg2_tok = QgramTokenizer()
            >>> qg2_tok.tokenize('database')
            ['da','at','ta','ab','ba','as','se']
            >>> qg2_tok.tokenize('a')
            []
            >>> qg3_tok = QgramTokenizer(3) 
            >>> qg3_tok.tokenize('database')
            ['dat', 'ata', 'tab', 'aba', 'bas', 'ase']
                      
        """
        utils.tok_check_for_none(input_string)
        utils.tok_check_for_string_input(input_string)

        qgram_list = []

        if len(input_string) < self.qval:
            return qgram_list

        qgram_list = [input_string[i:i + self.qval] for i in 
                          _range(len(input_string) - (self.qval - 1))]
        qgram_list = filter(None, qgram_list)

        if self.return_set:
            return utils.convert_bag_to_set(qgram_list)            

        return qgram_list
