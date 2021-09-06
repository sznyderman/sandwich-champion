import pytest
from sandwichchampion.domain.model import Sandwich, update_ratings


class TestSandwich:
    def test_name(self):
        sw = Sandwich("Grilled Cheese")

        assert sw.name == "Grilled Cheese"

    def test_initial_rating_is_1000(self):
        sw = Sandwich("Grilled Cheese")

        assert sw.rating == 1000

    @pytest.mark.parametrize(
        "starting_ratings, updated_ratings",
        (
            ((1000, 1000), (1010, 990)),
            ((2000, 2000), (2010, 1990)),
            ((1500, 2000), (1518.9, 1981.1)),
            ((2000, 1500), (2001.1, 1498.9)),
        ),
    )
    def test_update_rating(self, starting_ratings, updated_ratings):
        sw1 = Sandwich("sandwich 1")
        sw2 = Sandwich("sandwich 2")

        sw1.rating, sw2.rating = starting_ratings

        update_ratings(winner=sw1, loser=sw2)

        assert (sw1.rating, sw2.rating) == updated_ratings
