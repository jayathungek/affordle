from enum import Enum

from database import get_word_of_the_day, set_next_word

CORRECT = "+"
MISPLACED = "~"
WRONG = "-"


class State(Enum):
    WIN = 0
    LOSE = 1
    CONTINUE = 2


class Wordle:
    game_id: str
    solution: str
    guesses: int
    word_len: int
    max_guesses: int
    res: str

    def __init__(self, game_id, solution, word_len, max_guesses=6):
        self.game_id = game_id
        self.solution = solution
        self.guesses = 0
        self.word_len = word_len
        self.max_guesses = max_guesses
        self.res = ""

    @staticmethod
    def count_instances(word: str, char: str):
        n = 0
        for c in word:
            if c == char:
                n += 1
        return n

    def is_winning_res(self):
        for c in self.res:
            if c != CORRECT:
                return False
        return True

    def resolve_guess(self, guess: str):
        res = []
        char_counts = {char: self.count_instances(self.solution, char) for char in list(guess)}
        for idx in range(self.word_len):
            if guess[idx] == self.solution[idx]:
                res.append("+")
                char_counts[guess[idx]] -= 1
            else:
                res.append("-")

        for idx in range(self.word_len):
            if res[idx] == "-":
                if char_counts[guess[idx]] > 0:
                    res[idx] = "~"
                    char_counts[guess[idx]] -= 1

        self.res = "".join(res)

    def make_guess(self, guess: str):
        assert not (len(guess) > self.word_len), "Word is too long!"
        assert not (len(guess) < self.word_len), "Word is too short!"
        self.resolve_guess(guess)
        self.guesses += 1

        if self.is_winning_res():
            return State.WIN, self.res

        if self.guesses == self.max_guesses:
            return State.LOSE, self.res
        else:
            return State.CONTINUE, self.res


if __name__ == '__main__':
    wlen = 5
    word_of_the_day = get_word_of_the_day(wlen)
    print(word_of_the_day)
    w = Wordle(word_of_the_day, wlen)
    guess = input("Enter guess: ")
    state, rep = w.make_guess(guess)
    print(rep)
    while state == State.CONTINUE:
        guess = input("Enter guess: ")
        state, rep = w.make_guess(guess)
        print(rep)
        
    if state == State.WIN:
        print("You won :D")
    else:
        print("You lost :(")

    set_next_word(wlen)