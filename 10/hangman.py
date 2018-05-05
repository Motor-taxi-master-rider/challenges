import string
import sys
import types
from collections import defaultdict
from string import ascii_lowercase

from graphics import hang_graphics
from movies import get_movie as get_word  # keep interface generic

ASCII = list(ascii_lowercase)
HANG_GRAPHICS = list(hang_graphics())
ALLOWED_GUESSES = len(HANG_GRAPHICS)
PLACEHOLDER = '_'


class Hangman(object):
    def __init__(self, word: str):
        self._guessed_character = set()
        self._word: defaultdict = self._construct_word(word)
        self._guess: list = ['_' if character.upper() in string.ascii_uppercase else character
                             for character in word]
        self._hangman = self._hangman_popper()
        next(self._hangman)

    def _construct_word(self, word: str) -> defaultdict:
        character_dict = defaultdict(set)
        for index, character in enumerate(word):
            if character.strip():
                character_dict[character.upper()].add(index)
        return character_dict

    @types.coroutine
    def _hangman_popper(self):
        """print a hangman graph if guess is not right"""
        graphics = hang_graphics()
        graph = next(graphics)
        while True:
            guess = yield False
            if guess not in self._guessed_character:
                self._guessed_character.add(guess)
                if guess in self._word:
                    for index in self._word.pop(guess):
                        self._guess[index] = guess
                    if not self._word:
                        yield True
                else:
                    print(f'{guess} is not in the word!\n'
                          f'{graph}\n')
                    try:
                        graph = next(graphics)
                    except StopIteration:
                        raise NoChance

            else:
                print(f'You have guessed {guess}, please choose another character.')

    def current_puzzle(self, result=False):
        """if result True, fill up the answer"""
        if result:
            for character, indexs in self._word.items():
                for index in indexs:
                    self._guess[index] = character
        return ' '.join(self._guess)

    def guess(self, character: str):
        print(f'You guessed {character.upper()}.')
        result = self._hangman.send(character.upper())
        return result


class NoChance(Exception):
    pass


if __name__ == '__main__':
    if len(sys.argv) > 1:
        word = sys.argv[1]
    else:
        word = get_word()

    # init / call program
    han_man = Hangman(word)
    while True:
        print(f'Current puzzle: {han_man.current_puzzle()}')
        input_word = input('Please input the character: ')[0]
        try:
            if han_man.guess(input_word):
                print(f'You did it! The right answer is: \n{han_man.current_puzzle()}')
                break
        except NoChance:
            print('You have used up all your chance. Here is the answer:')
            print(f'{han_man.current_puzzle(result=True)}')
            break
