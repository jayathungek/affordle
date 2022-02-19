import random

import redis

from secret import get_db_url


def get_word_of_the_day(wordlen: int) -> str:
    cur_word_db = redis.from_url(get_db_url(0))
    words_db = redis.from_url(get_db_url(wordlen))
    return str(words_db.get(cur_word_db.get("cur_word")), "ascii")


def set_next_word(database: int):
    words_db = redis.from_url(get_db_url(database))
    cur_word_db = redis.from_url(get_db_url(0))
    cur_word = cur_word_db.get("cur_word")
    next_word = int(cur_word) + 1

    assert next_word < words_db.dbsize(), f"End of wordlist for DB {database}"

    cur_word_db.set("cur_word", next_word)


def reset_databases(seed: int = 0xdeadbeef):
    random.seed(seed)
    cur_word_db = redis.from_url(get_db_url(0))
    cur_word_db.set("cur_word", 0)
    for wlen in [4, 5, 6]:
        with open(f"words/words_{wlen}.txt") as fh:
            words = fh.readlines()
            random.shuffle(words)
            words_db = redis.from_url(get_db_url(wlen))
            for i, word in enumerate(words):
                words_db.set(i, word)