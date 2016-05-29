# coding=utf-8
"""Smith-Waterman measure"""

import numpy as np

from py_stringmatching import utils
from py_stringmatching.compat import _range
from py_stringmatching.similarity_measure.sequence_similarity_measure import \
                                                    SequenceSimilarityMeasure


def sim_ident(s1, s2):
    return int(s1 == s2)


class SmithWaterman(SequenceSimilarityMeasure):
    def __init__(self, gap_cost=1.0, sim_score=sim_ident):
        self.gap_cost = gap_cost
        self.sim_score = sim_score
        super(SmithWaterman, self).__init__()

    def get_raw_score(self, string1, string2):
        """
        Computes the Smith-Waterman measure between two strings.

        The Smith-Waterman algorithm performs local sequence alignment; that is, for determining similar regions
        between two strings. Instead of looking at the total sequence, the Smith–Waterman algorithm compares segments of
        all possible lengths and optimizes the similarity measure.


        Args:
            string1,string2 (str) : Input strings

        Returns:
            Smith-Waterman measure (float)

        Raises:
            TypeError : If the inputs are not strings or if one of the inputs is None.

        Examples:
            >>> sw = SmithWaterman()
            >>> sw.get_raw_score('cat', 'hat')
            2.0
            >>> sw = SmithWaterman(gap_cost=2.2)
            >>> sw.get_raw_score('dva', 'deeve')
            1.0
            >>> sw = SmithWaterman(gap_cost=1, sim_score=lambda s1, s2 : (2 if s1 == s2 else -1))
            >>> sw.get_raw_score('dva', 'deeve')
            2.0
            >>> sw = SmithWaterman(gap_cost=1.4, sim_score=lambda s1, s2 : (1.5 if s1 == s2 else 0.5))
            >>> sw.get_raw_score('GCATAGCU', 'GATTACA')
            6.5
        """
        # input validations
        utils.sim_check_for_none(string1, string2)
        utils.sim_check_for_string_inputs(string1, string2)

        dist_mat = np.zeros((len(string1) + 1, len(string2) + 1), dtype=np.float)
        max_value = 0
        # Smith Waterman DP calculations
        for i in _range(1, len(string1) + 1):
            for j in _range(1, len(string2) + 1):
                match = dist_mat[i - 1, j - 1] + self.sim_score(string1[i - 1], string2[j - 1])
                delete = dist_mat[i - 1, j] - self.gap_cost
                insert = dist_mat[i, j - 1] - self.gap_cost
                dist_mat[i, j] = max(0, match, delete, insert)
                max_value = max(max_value, dist_mat[i, j])

        return max_value
