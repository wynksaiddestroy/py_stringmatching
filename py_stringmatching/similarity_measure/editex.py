# coding=utf-8
"""Editex distance measure"""

from __future__ import division
from __future__ import unicode_literals
import unicodedata

import numpy as np

from py_stringmatching import utils
from py_stringmatching.compat import _range, _unicode
from py_stringmatching.similarity_measure.sequence_similarity_measure import \
                                                    SequenceSimilarityMeasure


class Editex(SequenceSimilarityMeasure):
    """Editex distance measure class.

    Parameters:
        match_cost (int): Weight to give the correct char match, default=0
        group_cost (int): Weight to give if the chars are in the same editex group, default=1
        mismatch_cost (int): Weight to give the incorrect char match, default=2
        local (boolean): Local variant on/off, default=False
    """
    def __init__(self, match_cost=0, group_cost=1, mismatch_cost=2,
                 local=False):
        self.match_cost = match_cost
        self.group_cost = group_cost
        self.mismatch_cost = mismatch_cost
        self.local = local
        super(Editex, self).__init__()

    def get_raw_score(self, string1, string2):
        """
        Computes the editex distance between two strings.

        As described on pages 3 & 4 of
        Zobel, Justin and Philip Dart. 1996. Phonetic string matching: Lessons from
        information retrieval. In: Proceedings of the ACM-SIGIR Conference on
        Research and Development in Information Retrieval, Zurich, Switzerland.
        166–173. http://goanna.cs.rmit.edu.au/~jz/fulltext/sigir96.pdf

        The local variant is based on
        Ring, Nicholas and Alexandra L. Uitdenbogerd. 2009. Finding ‘Lucy in
        Disguise’: The Misheard Lyric Matching Problem. In: Proceedings of the 5th
        Asia Information Retrieval Symposium, Sapporo, Japan. 157-167.
        http://www.seg.rmit.edu.au/research/download.php?manuscript=404

        Args:
            string1,string2 (str): Input strings

        Returns:
            Editex distance (int)

        Raises:
            TypeError : If the inputs are not strings

        Examples:
            >>> ed = Editex()
            >>> ed.get_raw_score('cat', 'hat')
            2
            >>> ed.get_raw_score('Niall', 'Neil')
            2
            >>> ed.get_raw_score('aluminum', 'Catalan')
            12
            >>> ed.get_raw_score('ATCG', 'TAGC')
            6

        References:
            * Abydos Library - https://github.com/chrislit/abydos/blob/master/abydos/distance.py

        """
        # input validations
        utils.sim_check_for_none(string1, string2)
        utils.sim_check_for_string_inputs(string1, string2)
        if utils.sim_check_for_exact_match(string1, string2):
            return 0

        # convert both the strings to NFKD normalized unicode
        string1 = unicodedata.normalize('NFKD', _unicode(string1.upper()))
        string2 = unicodedata.normalize('NFKD', _unicode(string2.upper()))

        # convert ß to SS (for Python2)
        string1 = string1.replace('ß', 'SS')
        string2 = string2.replace('ß', 'SS')

        if len(string1) == 0:
            return len(string2) * self.mismatch_cost
        if len(string2) == 0:
            return len(string1) * self.mismatch_cost

        d_mat = np.zeros((len(string1) + 1, len(string2) + 1), dtype=np.int)
        len1 = len(string1)
        len2 = len(string2)
        string1 = ' ' + string1
        string2 = ' ' + string2
        editex_helper = utils.Editex(self.match_cost, self.mismatch_cost,
                                     self.group_cost)

        if not self.local:
            for i in _range(1, len1 + 1):
                d_mat[i, 0] = d_mat[i - 1, 0] + editex_helper.d_cost(
                                                    string1[i - 1], string1[i])

        for j in _range(1, len2 + 1):
            d_mat[0, j] = d_mat[0, j - 1] + editex_helper.d_cost(string2[j - 1],
                                                                 string2[j])

        for i in _range(1, len1 + 1):
            for j in _range(1, len2 + 1):
                d_mat[i, j] = min(d_mat[i - 1, j] + editex_helper.d_cost(
                                                    string1[i - 1], string1[i]),
                                  d_mat[i, j - 1] + editex_helper.d_cost(
                                                    string2[j - 1], string2[j]),
                                  d_mat[i - 1, j - 1] + editex_helper.r_cost(
                                                        string1[i], string2[j]))

        return d_mat[len1, len2]

    def get_sim_score(self, string1, string2):
        """
        Computes the normalized editex similarity between two strings.

        Args:
            string1,string2 (str): Input strings

        Returns:
            Normalized editex similarity (float)

        Raises:
            TypeError : If the inputs are not strings

        Examples:
            >>> ed = Editex()
            >>> ed.get_sim_score('cat', 'hat')
            0.66666666666666674
            >>> ed.get_sim_score('Niall', 'Neil')
            0.80000000000000004
            >>> ed.get_sim_score('aluminum', 'Catalan')
            0.25
            >>> ed.get_sim_score('ATCG', 'TAGC')
            0.25

        References:
            * Abydos Library - https://github.com/chrislit/abydos/blob/master/abydos/distance.py
        """
        raw_score = self.get_raw_score(string1, string2)
        string1_len = len(string1)
        string2_len = len(string2)
        if string1_len == 0 and string2_len == 0:
            return 1.0
        return 1 - (raw_score / max(string1_len * self.mismatch_cost,
                                    string2_len * self.mismatch_cost))
