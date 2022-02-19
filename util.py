from typing import Optional

from affordle import Wordle


def get_game_by_id(games: [Wordle], game_id: str) -> Optional[Wordle]:
    for g in games:
        if g.game_id == game_id:
            return g
    return None


def remove_game_by_id(games: [Wordle], game_id: str):
    for i, g in enumerate(games):
        if g.game_id == game_id:
            games.__delitem__(i)