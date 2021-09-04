from sandwichchampion.domain.model import Sandwich


class TestSandwich:
    def test_name(self):
        sw = Sandwich("Grilled Cheese")

        assert sw.name == "Grilled Cheese"
