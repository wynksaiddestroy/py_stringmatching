"""Needleman-Wunsch measure"""

import numpy as np

from py_stringmatching import utils
from py_stringmatching.compat import _range
from py_stringmatching.similarity_measure.sequence_similarity_measure import \
                                                    SequenceSimilarityMeasure


def sim_ident(char1, char2):
    return int(char1 == char2)


class NeedlemanWunsch(SequenceSimilarityMeasure):
    """Needleman-Wunsch similarity measure class.

    Parameters:
        gap_cost (float): Cost of gap (defaults to 1.0)
        sim_func (function): Similarity function to give a score for the correspondence between characters. Defaults
                              to an identity function, where if two characters are same it returns 1.0 else returns 0.
    """
    def __init__(self, gap_cost=1.0, sim_func=sim_ident):
        self.gap_cost = gap_cost
        self.sim_func = sim_func
        super(NeedlemanWunsch, self).__init__()

    def get_raw_score(self, string1, string2):
        """
        Computes the Needleman-Wunsch measure between two strings.

        The Needleman-Wunsch generalizes the Levenshtein distance and considers global alignment between two strings.
        Specifically, it is computed by assigning a score to each alignment between two input strings and choosing the
        score of the best alignment, that is, the maximal score.

        An alignment between two strings is a set of correspondences between the characters of between them, allowing for
        gaps.

        Args:
            string1,string2 (str) : Input strings

        Returns:
            Needleman-Wunsch measure (float)

        Raises:
            TypeError : If the inputs are not strings or if one of the inputs is None.

        Examples:
            >>> nw = NeedlemanWunsch()
            >>> nw.get_raw_score('dva', 'deeva')
            1.0
            >>> nw = NeedlemanWunsch(gap_cost=0.0)
            >>> nw.get_raw_score('dva', 'deeve')
            2.0
            >>> nw = NeedlemanWunsch(gap_cost=1.0, sim_func=lambda s1, s2 : (2.0 if s1 == s2 else -1.0))
            >>> nw.get_raw_score('dva', 'deeve')
            1.0
            >>> nw = NeedlemanWunsch(gap_cost=0.5, sim_func=lambda s1, s2 : (1.0 if s1 == s2 else -1.0))
            >>> nw.get_raw_score('GCATGCUA', 'GATTACA')
            2.5

        """
        # input validations
        utils.sim_check_for_none(string1, string2)
        utils.sim_check_for_string_inputs(string1, string2)

        dist_mat = np.zeros((len(string1) + 1, len(string2) + 1),
                            dtype=np.float)

        # DP initialization
        for i in _range(len(string1) + 1):
            dist_mat[i, 0] = -(i * self.gap_cost)

        # DP initialization
        for j in _range(len(string2) + 1):
            dist_mat[0, j] = -(j * self.gap_cost)

        # Needleman-Wunsch DP calculation
        for i in _range(1, len(string1) + 1):
            for j in _range(1, len(string2) + 1):
                match = dist_mat[i - 1, j - 1] + self.sim_func(string1[i - 1],
                                                               string2[j - 1])
                delete = dist_mat[i - 1, j] - self.gap_cost
                insert = dist_mat[i, j - 1] - self.gap_cost
                dist_mat[i, j] = max(match, delete, insert)

        return dist_mat[dist_mat.shape[0] - 1, dist_mat.shape[1] - 1]
