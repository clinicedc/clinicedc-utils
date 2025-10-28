from decimal import Decimal
from unittest import TestCase

from clinicedc_utils import round_half_away_from_zero


class TestCalculators(TestCase):
    def test_round_up(self):
        self.assertEqual(round_half_away_from_zero(1.5, 0), 2)
        self.assertEqual(round_half_away_from_zero(1.55, 1), 1.6)
        self.assertEqual(round_half_away_from_zero(1.54, 1), 1.5)
        self.assertEqual(round_half_away_from_zero(1.555, 2), 1.56)
        self.assertEqual(round_half_away_from_zero(1.555, 2), 1.56)

        self.assertEqual(round_half_away_from_zero(-1.5, 0), -2)
        self.assertEqual(round_half_away_from_zero(-1.55, 1), -1.6)
        self.assertEqual(round_half_away_from_zero(-1.54, 1), -1.5)
        self.assertEqual(round_half_away_from_zero(-1.555, 2), -1.56)
        self.assertEqual(round_half_away_from_zero(-1.5554, 3), -1.555)

        self.assertEqual(round_half_away_from_zero(Decimal("1.5"), 0), Decimal(2))
        self.assertEqual(round_half_away_from_zero(Decimal("1.55"), 1), Decimal("1.6"))
        self.assertEqual(round_half_away_from_zero(Decimal("1.54"), 1), Decimal("1.5"))
        self.assertEqual(round_half_away_from_zero(Decimal("1.555"), 2), Decimal("1.56"))
        self.assertEqual(round_half_away_from_zero(Decimal("1.5554"), 3), Decimal("1.555"))
