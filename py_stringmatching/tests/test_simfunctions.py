from __future__ import unicode_literals

import math
import unittest

from nose.tools import *


# sequence based similarity measures
from py_stringmatching.simfunctions import levenshtein, jaro, jaro_winkler, hamming_distance, needleman_wunsch, \
    smith_waterman, affine, editex, bag_distance, soundex
# token based similarity measures
from py_stringmatching.similarity_measure.cosine import Cosine
from py_stringmatching.similarity_measure.dice import Dice
from py_stringmatching.similarity_measure.jaccard import Jaccard
from py_stringmatching.similarity_measure.overlap_coefficient import OverlapCoefficient
from py_stringmatching.simfunctions import tfidf, soft_tfidf, generalized_jaccard, tversky_index
# hybrid similarity measures
from py_stringmatching.simfunctions import monge_elkan


# ---------------------- sequence based similarity measures  ----------------------


class AffineTestCases(unittest.TestCase):
    def test_valid_input(self):
        self.assertAlmostEqual(affine('dva', 'deeva'), 1.5)
        self.assertAlmostEqual(affine('dva', 'deeve', gap_start=2, gap_continuation=0.5), -0.5)
        self.assertAlmostEqual(
            affine('AAAGAATTCA', 'AAATCA', gap_continuation=0.2, sim_score=lambda s1, s2: (int(1 if s1 == s2 else 0))),
            4.4)
        self.assertAlmostEqual(
            affine(' ', ' ', gap_continuation=0.2, sim_score=lambda s1, s2: (int(1 if s1 == s2 else 0))), 1)
        self.assertEqual(affine('', 'deeva'), 0)

    @raises(TypeError)
    def test_invalid_input1(self):
        affine(None, 'MARHTA')

    @raises(TypeError)
    def test_invalid_input2(self):
        affine('MARHTA', None)

    @raises(TypeError)
    def test_invalid_input3(self):
        affine('MARHTA', 12.90)

    @raises(TypeError)
    def test_invalid_input4(self):
        affine(12.90, 'MARTHA')

    @raises(TypeError)
    def test_invalid_input5(self):
        affine(None, None)

    @raises(TypeError)
    def test_invalid_input6(self):
        affine(12.90, 12.90)

class BagDistanceTestCases(unittest.TestCase):
    def test_valid_input(self):
        self.assertEqual(bag_distance('a', ''), 1)
        self.assertEqual(bag_distance('', 'a'), 1)
        self.assertEqual(bag_distance('abc', ''), 3)
        self.assertEqual(bag_distance('', 'abc'), 3)
        self.assertEqual(bag_distance('', ''), 0)
        self.assertEqual(bag_distance('a', 'a'), 0)
        self.assertEqual(bag_distance('abc', 'abc'), 0)
        self.assertEqual(bag_distance('', 'a'), 1)
        self.assertEqual(bag_distance('a', 'ab'), 1)
        self.assertEqual(bag_distance('b', 'ab'), 1)
        self.assertEqual(bag_distance('ac', 'abc'), 1)
        self.assertEqual(bag_distance('abcdefg', 'xabxcdxxefxgx'), 6)
        self.assertEqual(bag_distance('a', ''), 1)
        self.assertEqual(bag_distance('ab', 'a'), 1)
        self.assertEqual(bag_distance('ab', 'b'), 1)
        self.assertEqual(bag_distance('abc', 'ac'), 1)
        self.assertEqual(bag_distance('xabxcdxxefxgx', 'abcdefg'), 6)
        self.assertEqual(bag_distance('a', 'b'), 1)
        self.assertEqual(bag_distance('ab', 'ac'), 1)
        self.assertEqual(bag_distance('ac', 'bc'), 1)
        self.assertEqual(bag_distance('abc', 'axc'), 1)
        self.assertEqual(bag_distance('xabxcdxxefxgx', '1ab2cd34ef5g6'), 6)
        self.assertEqual(bag_distance('example', 'samples'), 2)
        self.assertEqual(bag_distance('sturgeon', 'urgently'), 2)
        self.assertEqual(bag_distance('bag_distance', 'frankenstein'), 6)
        self.assertEqual(bag_distance('distance', 'difference'), 5)
        self.assertEqual(bag_distance('java was neat', 'scala is great'), 6)

    @raises(TypeError)
    def test_invalid_input1(self):
        bag_distance('a', None)

    @raises(TypeError)
    def test_invalid_input2(self):
        bag_distance(None, 'b')

    @raises(TypeError)
    def test_invalid_input3(self):
        bag_distance(None, None)

    @raises(TypeError)
    def test_invalid_input4(self):
        bag_distance('MARHTA', 12.90)

    @raises(TypeError)
    def test_invalid_input5(self):
        bag_distance(12.90, 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6(self):
        bag_distance(12.90, 12.90)

class EditexTestCases(unittest.TestCase):
    def test_valid_input(self):
        self.assertEqual(editex('MARTHA', 'MARTHA'), 0)
        self.assertEqual(editex('MARTHA', 'MARHTA'), 3)
        self.assertEqual(editex('ALIE', 'ALI'), 1)
        self.assertEqual(editex('ALIE', 'ALI', match_cost=2), 7)
        self.assertEqual(editex('ALIE', 'ALIF', mismatch_cost=2), 2)
        self.assertEqual(editex('ALIE', 'ALIF', mismatch_cost=1), 1)
        self.assertEqual(editex('ALIP', 'ALIF', mismatch_cost=3, group_cost=2), 2)
        self.assertEqual(editex('ALIe', 'ALIF', mismatch_cost=3, group_cost=2), 3)
        self.assertEqual(editex('WALIW', 'HALIH', mismatch_cost=3, group_cost=2, local=True), 6)
        self.assertEqual(editex('niall', 'nihal', local=True), 2)
        self.assertEqual(editex('nihal', 'niall', local=True), 2)
        self.assertEqual(editex('neal', 'nihl', local=True), 3)
        self.assertEqual(editex('nihl', 'neal', local=True), 3)


    @raises(TypeError)
    def test_invalid_input1(self):
        editex(None, 'MARHTA')

    @raises(TypeError)
    def test_invalid_input2(self):
        editex('MARHTA', None)

    @raises(TypeError)
    def test_invalid_input3(self):
        editex(None, None)

    @raises(TypeError)
    def test_invalid_input4(self):
        editex('MARHTA', 12.90)

    @raises(TypeError)
    def test_invalid_input5(self):
        editex(12.90, 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6(self):
        editex(12.90, 12.90)


class JaroTestCases(unittest.TestCase):
    def test_valid_input(self):
        # https://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance
        self.assertAlmostEqual(jaro('MARTHA', 'MARHTA'), 0.9444444444444445)
        self.assertAlmostEqual(jaro('DWAYNE', 'DUANE'), 0.8222222222222223)
        self.assertAlmostEqual(jaro('DIXON', 'DICKSONX'), 0.7666666666666666)
        self.assertEqual(jaro('', 'deeva'), 0)

    @raises(TypeError)
    def test_invalid_input1(self):
        jaro(None, 'MARHTA')

    @raises(TypeError)
    def test_invalid_input2(self):
        jaro('MARHTA', None)

    @raises(TypeError)
    def test_invalid_input3(self):
        jaro(None, None)

    @raises(TypeError)
    def test_invalid_input4(self):
        jaro('MARHTA', 12.90)

    @raises(TypeError)
    def test_invalid_input5(self):
        jaro(12.90, 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6(self):
        jaro(12.90, 12.90)


class JaroWinklerTestCases(unittest.TestCase):
    def test_valid_input(self):
        # https://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance
        self.assertAlmostEqual(jaro_winkler('MARTHA', 'MARHTA'), 0.9611111111111111)
        self.assertAlmostEqual(jaro_winkler('DWAYNE', 'DUANE'), 0.84)
        self.assertAlmostEqual(jaro_winkler('DIXON', 'DICKSONX'), 0.8133333333333332)

    @raises(TypeError)
    def test_invalid_input1(self):
        jaro_winkler(None, 'MARHTA')

    @raises(TypeError)
    def test_invalid_input2(self):
        jaro_winkler('MARHTA', None)

    @raises(TypeError)
    def test_invalid_input3(self):
        jaro_winkler(None, None)

    @raises(TypeError)
    def test_invalid_input4(self):
        jaro_winkler('MARHTA', 12.90)

    @raises(TypeError)
    def test_invalid_input5(self):
        jaro_winkler(12.90, 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6(self):
        jaro_winkler(12.90, 12.90)


class LevenshteinTestCases(unittest.TestCase):
    def test_valid_input(self):
        # http://oldfashionedsoftware.com/tag/levenshtein-distance/
        self.assertEqual(levenshtein('a', ''), 1)
        self.assertEqual(levenshtein('', 'a'), 1)
        self.assertEqual(levenshtein('abc', ''), 3)
        self.assertEqual(levenshtein('', 'abc'), 3)
        self.assertEqual(levenshtein('', ''), 0)
        self.assertEqual(levenshtein('a', 'a'), 0)
        self.assertEqual(levenshtein('abc', 'abc'), 0)
        self.assertEqual(levenshtein('', 'a'), 1)
        self.assertEqual(levenshtein('a', 'ab'), 1)
        self.assertEqual(levenshtein('b', 'ab'), 1)
        self.assertEqual(levenshtein('ac', 'abc'), 1)
        self.assertEqual(levenshtein('abcdefg', 'xabxcdxxefxgx'), 6)
        self.assertEqual(levenshtein('a', ''), 1)
        self.assertEqual(levenshtein('ab', 'a'), 1)
        self.assertEqual(levenshtein('ab', 'b'), 1)
        self.assertEqual(levenshtein('abc', 'ac'), 1)
        self.assertEqual(levenshtein('xabxcdxxefxgx', 'abcdefg'), 6)
        self.assertEqual(levenshtein('a', 'b'), 1)
        self.assertEqual(levenshtein('ab', 'ac'), 1)
        self.assertEqual(levenshtein('ac', 'bc'), 1)
        self.assertEqual(levenshtein('abc', 'axc'), 1)
        self.assertEqual(levenshtein('xabxcdxxefxgx', '1ab2cd34ef5g6'), 6)
        self.assertEqual(levenshtein('example', 'samples'), 3)
        self.assertEqual(levenshtein('sturgeon', 'urgently'), 6)
        self.assertEqual(levenshtein('levenshtein', 'frankenstein'), 6)
        self.assertEqual(levenshtein('distance', 'difference'), 5)
        self.assertEqual(levenshtein('java was neat', 'scala is great'), 7)

    @raises(TypeError)
    def test_invalid_input1(self):
        levenshtein('a', None)

    @raises(TypeError)
    def test_invalid_input2(self):
        levenshtein(None, 'b')

    @raises(TypeError)
    def test_invalid_input3(self):
        levenshtein(None, None)

    @raises(TypeError)
    def test_invalid_input4(self):
        levenshtein('MARHTA', 12.90)

    @raises(TypeError)
    def test_invalid_input5(self):
        levenshtein(12.90, 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6(self):
        levenshtein(12.90, 12.90)


class HammingDistanceTestCases(unittest.TestCase):
    def test_valid_input(self):
        self.assertEqual(hamming_distance('-789', 'john'), 4)
        self.assertEqual(hamming_distance('a', '*'), 1)
        self.assertEqual(hamming_distance('b', 'a'), 1)
        self.assertEqual(hamming_distance('abc', 'p q'), 3)
        self.assertEqual(hamming_distance('karolin', 'kathrin'), 3)
        self.assertEqual(hamming_distance('KARI', 'kari'), 4)

    def test_valid_input_compatibility(self):
        self.assertEqual(hamming_distance(u'karolin', u'kathrin'), 3)
        self.assertEqual(hamming_distance(u'', u''), 0)
        # str_1 = u'foo'.encode(encoding='UTF-8', errors='strict')
        # str_2 = u'bar'.encode(encoding='UTF-8', errors='strict')
        # self.assertEqual(hamming_distance(str_1, str_2), 3) # check with Ali - python 3 returns type error
        # self.assertEqual(hamming_distance(str_1, str_1), 0) # check with Ali - python 3 returns type error

    @raises(TypeError)
    def test_invalid_input1(self):
        hamming_distance('a', None)

    @raises(TypeError)
    def test_invalid_input2(self):
        hamming_distance(None, 'b')

    @raises(TypeError)
    def test_invalid_input3(self):
        hamming_distance(None, None)

    @raises(ValueError)
    def test_invalid_input4(self):
        hamming_distance('a', '')

    @raises(ValueError)
    def test_invalid_input5(self):
        hamming_distance('', 'This is a long string')

    @raises(ValueError)
    def test_invalid_input6(self):
        hamming_distance('ali', 'alex')

    @raises(TypeError)
    def test_invalid_input7(self):
        hamming_distance('MA', 12)

    @raises(TypeError)
    def test_invalid_input8(self):
        hamming_distance(12, 'MA')

    @raises(TypeError)
    def test_invalid_input9(self):
        hamming_distance(12, 12)


class NeedlemanWunschTestCases(unittest.TestCase):
    def test_valid_input(self):
        self.assertEqual(needleman_wunsch('dva', 'deeva'), 1.0)
        self.assertEqual(needleman_wunsch('dva', 'deeve', 0.0), 2.0)
        self.assertEqual(needleman_wunsch('dva', 'deeve', 1.0, sim_score=lambda s1, s2: (2 if s1 == s2 else -1)), 1.0)
        self.assertEqual(
            needleman_wunsch('GCATGCUA', 'GATTACA', gap_cost=0.5,
                             sim_score=lambda s1, s2: (1 if s1 == s2 else -1)),
            2.5)

    @raises(TypeError)
    def test_invalid_input1(self):
        needleman_wunsch('a', None)

    @raises(TypeError)
    def test_invalid_input2(self):
        needleman_wunsch(None, 'b')

    @raises(TypeError)
    def test_invalid_input3(self):
        needleman_wunsch(None, None)

    @raises(TypeError)
    def test_invalid_input4(self):
        needleman_wunsch(['a'], 'b')

    @raises(TypeError)
    def test_invalid_input5(self):
        needleman_wunsch('a', ['b'])

    @raises(TypeError)
    def test_invalid_input6(self):
        needleman_wunsch(['a'], ['b'])



class SmithWatermanTestCases(unittest.TestCase):
    def test_valid_input(self):
        self.assertEqual(smith_waterman('cat', 'hat'), 2.0)
        self.assertEqual(smith_waterman('dva', 'deeve', 2.2), 1.0)
        self.assertEqual(smith_waterman('dva', 'deeve', 1, sim_score=lambda s1, s2: (2 if s1 == s2 else -1)), 2.0)
        self.assertEqual(
            smith_waterman('GCATGCU', 'GATTACA', gap_cost=1, sim_score=lambda s1, s2: (int(1 if s1 == s2 else -1))),
            2.0)
        self.assertEqual(
            smith_waterman('GCATAGCU', 'GATTACA', gap_cost=1.4, sim_score=lambda s1, s2: (1.5 if s1 == s2 else 0.5)),
            6.5)

    @raises(TypeError)
    def test_invalid_input1(self):
        smith_waterman('a', None)

    @raises(TypeError)
    def test_invalid_input2(self):
        smith_waterman(None, 'b')

    @raises(TypeError)
    def test_invalid_input3(self):
        smith_waterman(None, None)

    @raises(TypeError)
    def test_invalid_input4(self):
        smith_waterman('MARHTA', 12)

    @raises(TypeError)
    def test_invalid_input5(self):
        smith_waterman(12, 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6(self):
        smith_waterman(12, 12)
class SoundexTestCases(unittest.TestCase):
    def test_valid_input(self):
        self.assertEqual(soundex('Robert', 'Rupert'), 1)
        self.assertEqual(soundex('Sue', 'S'), 1)
        self.assertEqual(soundex('robert', 'rupert'), 1)
        self.assertEqual(soundex('Gough', 'goff'), 0)
        self.assertEqual(soundex('gough', 'Goff'), 0)
        self.assertEqual(soundex('ali', 'a,,,li'), 1)
        self.assertEqual(soundex('Jawornicki', 'Yavornitzky'), 0)

    @raises(TypeError)
    def test_invalid_input1(self):
        soundex('a', None)

    @raises(TypeError)
    def test_invalid_input2(self):
        soundex(None, 'b')

    @raises(TypeError)
    def test_invalid_input3(self):
        soundex(None, None)

    @raises(ValueError)
    def test_invalid_input4(self):
        soundex('a', '')

    @raises(ValueError)
    def test_invalid_input5(self):
        soundex('', 'This is a long string')

    @raises(TypeError)
    def test_invalid_input7(self):
        soundex('xyz', [''])


# ---------------------- token based similarity measures  ----------------------

# ---------------------- set based similarity measures  ----------------------
class OverlapCoefficientTestCases(unittest.TestCase):
    def setUp(self):
        self.oc = OverlapCoefficient()

    def test_valid_input(self):
        self.assertEqual(self.oc.get_raw_score([], []), 1.0)
        self.assertEqual(self.oc.get_raw_score(['data', 'science'], ['data']),
                         1.0 / min(2.0, 1.0))
        self.assertEqual(self.oc.get_raw_score(['data', 'science'],
                                               ['science', 'good']), 1.0 / min(2.0, 3.0))
        self.assertEqual(self.oc.get_raw_score([], ['data']), 0)
        self.assertEqual(self.oc.get_raw_score(['data', 'data', 'science'],
                                               ['data', 'management']), 1.0 / min(3.0, 2.0))
        self.assertEqual(self.oc.get_sim_score(['data', 'science'], ['data']),
                         1.0 / min(2.0, 1.0))

    @raises(TypeError)
    def test_invalid_input1(self):
        self.oc.get_raw_score(['a'], None)

    @raises(TypeError)
    def test_invalid_input2(self):
        self.oc.get_raw_score(None, ['b'])

    @raises(TypeError)
    def test_invalid_input3(self):
        self.oc.get_raw_score(None, None)

    @raises(TypeError)
    def test_invalid_input4(self):
        self.oc.get_raw_score(['MARHTA'], 'MARTHA')

    @raises(TypeError)
    def test_invalid_input5(self):
        self.oc.get_raw_score('MARHTA', ['MARTHA'])

    @raises(TypeError)
    def test_invalid_input6(self):
        self.oc.get_raw_score('MARTHA', 'MARTHA')


class DiceTestCases(unittest.TestCase):
    def setUp(self):
        self.dice = Dice()

    def test_valid_input(self):
        self.assertEqual(self.dice.get_raw_score(['data', 'science'], ['data']),
                         2 * 1.0 / 3.0)
        self.assertEqual(self.dice.get_raw_score(['data', 'science'], ['science', 'good']),
                         2 * 1.0 / 4.0)
        self.assertEqual(self.dice.get_raw_score([], ['data']), 0)
        self.assertEqual(self.dice.get_raw_score(['data', 'data', 'science'],
                                                 ['data', 'management']), 2 * 1.0 / 4.0)
        self.assertEqual(self.dice.get_raw_score(['data', 'management'],
                                                 ['data', 'data', 'science']), 2 * 1.0 / 4.0)
        self.assertEqual(self.dice.get_raw_score([], []), 1.0)
        self.assertEqual(self.dice.get_raw_score(['a', 'b'], ['b', 'a']), 1.0)
        self.assertEqual(self.dice.get_raw_score(set([]), set([])), 1.0)
        self.assertEqual(self.dice.get_raw_score({1, 1, 2, 3, 4}, {2, 3, 4, 5, 6, 7, 7, 8}),
                         2 * 3.0 / 11.0)
        self.assertEqual(self.dice.get_sim_score(['data', 'science'], ['data']),
                         2 * 1.0 / 3.0)

    @raises(TypeError)
    def test_invalid_input1(self):
        self.dice.get_raw_score(1, 1)

    @raises(TypeError)
    def test_invalid_input2(self):
        self.dice.get_raw_score(['a'], None)

    @raises(TypeError)
    def test_invalid_input3(self):
        self.dice.get_raw_score(None, ['b'])

    @raises(TypeError)
    def test_invalid_input4(self):
        self.dice.get_raw_score(None, None)

    @raises(TypeError)
    def test_invalid_input5(self):
        self.dice.get_raw_score(None, 'MARHTA')

    @raises(TypeError)
    def test_invalid_input6(self):
        self.dice.get_raw_score('MARHTA', None)

    @raises(TypeError)
    def test_invalid_input7(self):
        self.dice.get_raw_score('MARHTA', 'MARTHA')


class JaccardTestCases(unittest.TestCase):
    def setUp(self):
        self.jac = Jaccard()

    def test_valid_input(self):
        self.assertEqual(self.jac.get_raw_score(['data', 'science'], ['data']),
                         1.0 / 2.0)
        self.assertEqual(self.jac.get_raw_score(['data', 'science'],
                                                ['science', 'good']), 1.0 / 3.0)
        self.assertEqual(self.jac.get_raw_score([], ['data']), 0)
        self.assertEqual(self.jac.get_raw_score(['data', 'data', 'science'],
                             ['data', 'management']), 1.0 / 3.0)
        self.assertEqual(self.jac.get_raw_score(['data', 'management'],
                             ['data', 'data', 'science']), 1.0 / 3.0)
        self.assertEqual(self.jac.get_raw_score([], []), 1.0)
        self.assertEqual(self.jac.get_raw_score(set([]), set([])), 1.0)
        self.assertEqual(self.jac.get_raw_score({1, 1, 2, 3, 4},
                             {2, 3, 4, 5, 6, 7, 7, 8}), 3.0 / 8.0)
        self.assertEqual(self.jac.get_sim_score(['data', 'science'], ['data']),
                         1.0 / 2.0)

    @raises(TypeError)
    def test_invalid_input1(self):
        self.jac.get_raw_score(1, 1)

    @raises(TypeError)
    def test_invalid_input2(self):
        self.jac.get_raw_score(['a'], None)

    @raises(TypeError)
    def test_invalid_input3(self):
        self.jac.get_raw_score(None, ['b'])

    @raises(TypeError)
    def test_invalid_input4(self):
        self.jac.get_raw_score(None, None)

    @raises(TypeError)
    def test_invalid_input5(self):
        self.jac.get_raw_score(['MARHTA'], 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6(self):
        self.jac.get_raw_score('MARHTA', ['MARTHA'])

    @raises(TypeError)
    def test_invalid_input7(self):
        self.jac.get_raw_score('MARTHA', 'MARTHA')


class GeneralizedJaccardTestCases(unittest.TestCase):
    def test_valid_input(self):
        self.assertEqual(generalized_jaccard([''], ['']), 1.0)  # need to check this

        self.assertEqual(generalized_jaccard([''], ['a']), 0.0)
        self.assertEqual(generalized_jaccard(['a'], ['a']), 1.0)

        self.assertEqual(generalized_jaccard(['Niall'], ['Neal']), 0.7833333333333333)
        self.assertEqual(generalized_jaccard(['Niall'], ['Njall', 'Neal']), 0.43333333333333335)
        self.assertEqual(generalized_jaccard(['Niall'], ['Neal', 'Njall']), 0.43333333333333335)
        self.assertEqual(generalized_jaccard(['Comput.', 'Sci.', 'and', 'Eng.', 'Dept.,', 'University', 'of', 'California,', 'San', 'Diego'],
                                     ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego']), 0.6800468975468975)
        self.assertEqual(
            generalized_jaccard(['Comput.', 'Sci.', 'and', 'Eng.', 'Dept.,', 'University', 'of', 'California,', 'San', 'Diego'],
                        ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego'],
                        sim_func=jaro_winkler), 0.7220003607503608)
        self.assertEqual(
            generalized_jaccard(['Comp', 'Sci.', 'and', 'Engr', 'Dept.,', 'Universty', 'of', 'Cal,', 'San', 'Deigo'],
                        ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego'],
                        sim_func=jaro_winkler), 0.7075277777777778)
        self.assertEqual(
            generalized_jaccard(['Comp', 'Sci.', 'and', 'Engr', 'Dept.,', 'Universty', 'of', 'Cal,', 'San', 'Deigo'],
                        ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego'],
                        sim_func=jaro_winkler, threshold=0.8), 0.45810185185185187)
        self.assertEqual(generalized_jaccard([], ['Nigel']), 0.0)

    @raises(TypeError)
    def test_invalid_input1(self):
        generalized_jaccard(1, 1)

    @raises(TypeError)
    def test_invalid_input2(self):
        generalized_jaccard(None, ['b'])

    @raises(TypeError)
    def test_invalid_input3(self):
        generalized_jaccard(None, None)

    @raises(TypeError)
    def test_invalid_input4(self):
        generalized_jaccard("temp", "temp")

    @raises(TypeError)
    def test_invalid_input5(self):
        generalized_jaccard(['temp'], 'temp')

    @raises(TypeError)
    def test_invalid_input6(self):
        generalized_jaccard(['a'], None)

    @raises(TypeError)
    def test_invalid_input7(self):
        generalized_jaccard('temp', ['temp'])

    @raises(ValueError)
    def test_invalid_sim_measure(self):
        generalized_jaccard(['Comp', 'Sci.', 'and', 'Engr', 'Dept.,', 'Universty', 'of', 'Cal,', 'San', 'Deigo'],
                    ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego'],
                    sim_func=needleman_wunsch, threshold=0.8)


class CosineTestCases(unittest.TestCase):
    def setUp(self):
        self.cos = Cosine()

    def test_valid_input(self):
        self.assertEqual(self.cos.get_raw_score(['data', 'science'], ['data']), 1.0 / (math.sqrt(2) * math.sqrt(1)))
        self.assertEqual(self.cos.get_raw_score(['data', 'science'], ['science', 'good']),
                         1.0 / (math.sqrt(2) * math.sqrt(2)))
        self.assertEqual(self.cos.get_raw_score([], ['data']), 0.0)
        self.assertEqual(self.cos.get_raw_score(['data', 'data', 'science'], ['data', 'management']),
                         1.0 / (math.sqrt(2) * math.sqrt(2)))
        self.assertEqual(self.cos.get_raw_score(['data', 'management'], ['data', 'data', 'science']),
                         1.0 / (math.sqrt(2) * math.sqrt(2)))
        self.assertEqual(self.cos.get_raw_score([], []), 1.0)
        self.assertEqual(self.cos.get_raw_score(set([]), set([])), 1.0)
        self.assertEqual(self.cos.get_raw_score({1, 1, 2, 3, 4}, {2, 3, 4, 5, 6, 7, 7, 8}),
                         3.0 / (math.sqrt(4) * math.sqrt(7)))
        self.assertEqual(self.cos.get_sim_score(['data', 'science'], ['data']), 1.0 / (math.sqrt(2) * math.sqrt(1)))

    @raises(TypeError)
    def test_invalid_input1(self):
        self.cos.get_raw_score(1, 1)

    @raises(TypeError)
    def test_invalid_input4(self):
        self.cos.get_raw_score(['a'], None)

    @raises(TypeError)
    def test_invalid_input2(self):
        self.cos.get_raw_score(None, ['b'])

    @raises(TypeError)
    def test_invalid_input3(self):
        self.cos.get_raw_score(None, None)

    @raises(TypeError)
    def test_invalid_input5(self):
        self.cos.get_raw_score(['MARHTA'], 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6(self):
        self.cos.get_raw_score('MARHTA', ['MARTHA'])

    @raises(TypeError)
    def test_invalid_input7(self):
        self.cos.get_raw_score('MARTHA', 'MARTHA')


class TfidfTestCases(unittest.TestCase):
    def test_valid_input(self):
        self.assertEqual(tfidf(['a', 'b', 'a'], ['a', 'c'], [['a', 'b', 'a'], ['a', 'c'], ['a'], ['b']], True),
                         0.11166746710505392)
        self.assertEqual(tfidf(['a', 'b', 'a'], ['a', 'c'], [['a', 'b', 'a'], ['a', 'c'], ['a']]), 0.17541160386140586)
        self.assertEqual(tfidf(['a', 'b', 'a'], ['a'], [['a', 'b', 'a'], ['a', 'c'], ['a']]), 0.5547001962252291)
        self.assertEqual(tfidf(['a', 'b', 'a'], ['a']), 0.7071067811865475)
        self.assertEqual(tfidf(['a', 'b', 'a'], ['a'], [['x', 'y'], ['w'], ['q']]), 0.0)
        self.assertEqual(tfidf(['a', 'b', 'a'], ['a']), 0.7071067811865475)
        self.assertEqual(tfidf(['a', 'b', 'a'], ['a', 'b', 'a']), 1.0)
        self.assertEqual(tfidf([], ['a', 'b', 'a']), 0.0)

    @raises(TypeError)
    def test_invalid_input1(self):
        tfidf(1, 1)

    @raises(TypeError)
    def test_invalid_input4(self):
        tfidf(['a'], None)

    @raises(TypeError)
    def test_invalid_input2(self):
        tfidf(None, ['b'])

    @raises(TypeError)
    def test_invalid_input3(self):
        tfidf(None, None)

    @raises(TypeError)
    def test_invalid_input5(self):
        tfidf(['MARHTA'], 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6(self):
        tfidf('MARHTA', ['MARTHA'])

    @raises(TypeError)
    def test_invalid_input7(self):
        tfidf('MARTHA', 'MARTHA')
class TverskyIndexTestCases(unittest.TestCase):
    def test_valid_input(self):
        self.assertEqual(tversky_index(['data', 'science'], ['data'], 0.5, 0.5), 1.0 / (1.0 + 0.5*1 + 0.5*0))
        self.assertEqual(tversky_index(['data', 'science'], ['science', 'good']), 1.0 / (1.0 + 0.5*1 + 0.5*1))
        self.assertEqual(tversky_index([], ['data']), 0)
        self.assertEqual(tversky_index(['data', 'data', 'science'], ['data', 'management'], 0.7, 0.8),
                         1.0 / (1.0 + 0.7*1 + 0.8*1))
        self.assertEqual(tversky_index(['data', 'management', 'science'], ['data', 'data', 'science'], 0.2, 0.4),
                         2.0 / (2.0 + 0.2*1 + 0))
        self.assertEqual(tversky_index([], []), 1.0)
        self.assertEqual(tversky_index(['a', 'b'], ['b', 'a'], 0.9, 0.8), 1.0)
        self.assertEqual(tversky_index(['a', 'b'], ['b', 'a']), 1.0)
        self.assertEqual(tversky_index(set([]), set([])), 1.0)
        self.assertEqual(tversky_index({1, 1, 2, 3, 4}, {2, 3, 4, 5, 6, 7, 7, 8}, 0.45, 0.85),
                         3.0 / (3.0 + 0.45*1 + 0.85*4))

    @raises(TypeError)
    def test_invalid_input1(self):
        tversky_index(1, 1)

    @raises(TypeError)
    def test_invalid_input2(self):
        tversky_index(['a'], None)

    @raises(TypeError)
    def test_invalid_input3(self):
        tversky_index(None, ['b'])

    @raises(TypeError)
    def test_invalid_input4(self):
        tversky_index(None, None)

    @raises(TypeError)
    def test_invalid_input5(self):
        tversky_index(None, 'MARHTA')

    @raises(TypeError)
    def test_invalid_input6(self):
        tversky_index('MARHTA', None)

    @raises(TypeError)
    def test_invalid_input7(self):
        tversky_index('MARHTA', 'MARTHA')

    @raises(ValueError)
    def test_invalid_input8(self):
        tversky_index(['MARHTA'], ['MARTHA'], 0.5, -0.9)

    @raises(ValueError)
    def test_invalid_input9(self):
        tversky_index(['MARHTA'], ['MARTHA'], -0.5, 0.9)

    @raises(ValueError)
    def test_invalid_input10(self):
        tversky_index(['MARHTA'], ['MARTHA'], -0.5, -0.9)

# ---------------------- bag based similarity measures  ----------------------
# class CosineTestCases(unittest.TestCase):
#     def test_valid_input(self):
#         NONQ_FROM = 'The quick brown fox jumped over the lazy dog.'
#         NONQ_TO = 'That brown dog jumped over the fox.'
#         self.assertEqual(cosine([], []), 1) # check-- done. both simmetrics, abydos return 1.
#         self.assertEqual(cosine(['the', 'quick'], []), 0)
#         self.assertEqual(cosine([], ['the', 'quick']), 0)
#         self.assertAlmostEqual(cosine(whitespace(NONQ_TO), whitespace(NONQ_FROM)),
#                                4/math.sqrt(9*7))
#
#     @raises(TypeError)
#     def test_invalid_input1(self):
#         cosine(['a'], None)
#     @raises(TypeError)
#     def test_invalid_input2(self):
#         cosine(None, ['b'])
#     @raises(TypeError)
#     def test_invalid_input3(self):
#         cosine(None, None)


# ---------------------- hybrid similarity measure  ----------------------

class Soft_TfidfTestCases(unittest.TestCase):
    def test_valid_input(self):
        self.assertEqual(soft_tfidf(['a', 'b', 'a'], ['a', 'c'], [['a', 'b', 'a'], ['a', 'c'], ['a']], sim_func=jaro,
                                    threshold=0.8), 0.17541160386140586)
        self.assertEqual(soft_tfidf(['a', 'b', 'a'], ['a'], [['a', 'b', 'a'], ['a', 'c'], ['a']],
                                    threshold=0.9), 0.5547001962252291)
        self.assertEqual(soft_tfidf(['a', 'b', 'a'], ['a'], [['x', 'y'], ['w'], ['q']]), 0.0)
        self.assertEqual(soft_tfidf(['aa', 'bb', 'a'], ['ab', 'ba'], sim_func=affine, threshold=0.6),
                         0.81649658092772592)
        self.assertEqual(soft_tfidf(['a', 'b', 'a'], ['a', 'b', 'a']), 1.0)
        self.assertEqual(soft_tfidf([], ['a', 'b', 'a']), 0.0)

    @raises(TypeError)
    def test_invalid_input1(self):
        soft_tfidf(1, 1)

    @raises(TypeError)
    def test_invalid_input4(self):
        soft_tfidf(['a'], None)

    @raises(TypeError)
    def test_invalid_input2(self):
        soft_tfidf(None, ['b'])

    @raises(TypeError)
    def test_invalid_input3(self):
        soft_tfidf(None, None)

    @raises(TypeError)
    def test_invalid_input5(self):
        soft_tfidf(['MARHTA'], 'MARTHA')

    @raises(TypeError)
    def test_invalid_input6(self):
        soft_tfidf('MARHTA', ['MARTHA'])

    @raises(TypeError)
    def test_invalid_input7(self):
        soft_tfidf('MARTHA', 'MARTHA')


class MongeElkanTestCases(unittest.TestCase):
    def test_valid_input(self):
        self.assertEqual(monge_elkan([''], ['']), 1.0)  # need to check this

        self.assertEqual(monge_elkan([''], ['a']), 0.0)
        self.assertEqual(monge_elkan(['a'], ['a']), 1.0)

        self.assertEqual(monge_elkan(['Niall'], ['Neal']), 0.8049999999999999)
        self.assertEqual(monge_elkan(['Niall'], ['Njall']), 0.88)
        self.assertEqual(monge_elkan(['Comput.', 'Sci.', 'and', 'Eng.', 'Dept.,', 'University', 'of', 'California,', 'San', 'Diego'],
                                     ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego']), 0.8364448051948052)
        self.assertEqual(
            monge_elkan(['Comput.', 'Sci.', 'and', 'Eng.', 'Dept.,', 'University', 'of', 'California,', 'San', 'Diego'],
                        ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego'],
                        sim_func=needleman_wunsch), 2.0)
        self.assertEqual(
            monge_elkan(['Comput.', 'Sci.', 'and', 'Eng.', 'Dept.,', 'University', 'of', 'California,', 'San', 'Diego'],
                        ['Department', 'of', 'Computer', 'Science,', 'Univ.', 'Calif.,', 'San', 'Diego'],
                        sim_func=affine), 2.25)
        self.assertEqual(monge_elkan(['Niall'], ['Niel']), 0.8266666666666667)
        self.assertEqual(monge_elkan(['Niall'], ['Nigel']), 0.7866666666666667)
        self.assertEqual(monge_elkan([], ['Nigel']), 0.0)

    @raises(TypeError)
    def test_invalid_input1(self):
        monge_elkan(1, 1)

    @raises(TypeError)
    def test_invalid_input2(self):
        monge_elkan(None, ['b'])

    @raises(TypeError)
    def test_invalid_input3(self):
        monge_elkan(None, None)

    @raises(TypeError)
    def test_invalid_input4(self):
        monge_elkan("temp", "temp")

    @raises(TypeError)
    def test_invalid_input5(self):
        monge_elkan(['temp'], 'temp')

    @raises(TypeError)
    def test_invalid_input6(self):
        monge_elkan(['a'], None)

    @raises(TypeError)
    def test_invalid_input7(self):
        monge_elkan('temp', ['temp'])
