import itertools
import unittest

from game import (_get_permutations_draw, _validation, calc_word_value,
                  draw_letters, get_possible_dict_words, max_word_value)

NUM_LETTERS = 7
TEST_WORDS = ('bob', 'julian', 'pybites', 'quit', 'barbeque')


class TestGame(unittest.TestCase):

    def setUp(self):
        self.draw = draw_letters()

    def test_draw_letters(self):
        letter_str = ''.join(self.draw)
        self.assertRegex(letter_str, r'^[A-Z]{%s}$' % NUM_LETTERS)

    # from ch01
    def test_calc_word_value(self):
        self.assertEqual(calc_word_value('bob'), 7)
        self.assertEqual(calc_word_value('JuliaN'), 13)

    # from ch01
    def test_max_word_value(self):
        self.assertEqual(max_word_value(TEST_WORDS), 'barbeque')

    def test_get_permutations_draw(self):
        gen_permutations_n_letters = sum(
            len(set(itertools.permutations(self.draw, n))) for n in range(1, len(self.draw) + 1))
        game_permutations = len(list(_get_permutations_draw(self.draw)))
        self.assertEqual(gen_permutations_n_letters, game_permutations)
        alist = range(1, 8)
        gen_permutations_any_list = sum(len(set(itertools.permutations(alist, n))) for n in range(1, len(alist) + 1))
        game_permutations = len(list(_get_permutations_draw(alist)))
        self.assertEqual(gen_permutations_any_list, game_permutations)

    def test_get_possible_dict_words(self):
        self.fixed_draw = list('garytev'.upper())
        words = get_possible_dict_words(self.fixed_draw)
        self.assertEqual(len(words), 137)

    def test_validation(self):
        draw = list('garytev'.upper())
        word = 'GARYTEV'
        self.assertFalse(_validation(word, draw))
        word = 'F'
        self.assertFalse(_validation(word, draw))
        word = 'GARETTA'
        self.assertFalse(_validation(word, draw))


if __name__ == "__main__":
    unittest.main()
