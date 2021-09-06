from __future__ import annotations


class Sandwich:
    def __init__(self, name: str):
        self.name = name
        self.rating = 1000


def update_ratings(winner: Sandwich, loser: Sandwich):
    def calculate_change():
        K = 20
        ratio = (loser.rating - winner.rating) / 400
        expected_score = 1 / (1 + 10 ** ratio)
        return round(K * (1 - expected_score), 1)

    change = calculate_change()
    winner.rating += change
    loser.rating -= change
