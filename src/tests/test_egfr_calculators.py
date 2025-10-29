from unittest import TestCase

from clinicedc_constants import (
    BLACK,
    FEMALE,
    MALE,
    MICROMOLES_PER_LITER,
    MILLIGRAMS_PER_DECILITER,
    NON_BLACK,
)

from clinicedc_utils import (
    EgfrCkdEpi2009,
    EgfrCkdEpi2021,
    EgfrCockcroftGault,
    convert_units,
    egfr_percent_change,
    round_half_away_from_zero,
)
from clinicedc_utils.constants import MW_CREATININE
from clinicedc_utils.exceptions import EgfrCalculatorError


class TestCalculators(TestCase):
    def test_creatinine_units(self):
        """U.S. units: 0.84 to 1.21 milligrams per deciliter (mg/dL);
        European units: 74.3 to 107 micromoles per liter (umol/L)
        """
        value = round_half_away_from_zero(
            convert_units(
                label="creatinine",
                value=0.84,
                units_from=MILLIGRAMS_PER_DECILITER,
                units_to=MICROMOLES_PER_LITER,
                mw=MW_CREATININE,  # g/mol
            ),
            1,
        )
        self.assertEqual(value, 74.3)
        self.assertEqual(
            round_half_away_from_zero(
                convert_units(
                    label="creatinine",
                    value=1.21,
                    units_from=MILLIGRAMS_PER_DECILITER,
                    units_to=MICROMOLES_PER_LITER,
                    mw=MW_CREATININE,  # g/mol
                ),
                1,
            ),
            107.0,
        )
        self.assertEqual(
            round_half_away_from_zero(
                convert_units(
                    label="creatinine",
                    value=74.3,
                    units_from=MICROMOLES_PER_LITER,
                    units_to=MILLIGRAMS_PER_DECILITER,
                    mw=MW_CREATININE,  # g/mol
                ),
                2,
            ),
            0.84,
        )
        self.assertEqual(
            round_half_away_from_zero(
                convert_units(
                    label="creatinine",
                    value=107.0,
                    units_from=MICROMOLES_PER_LITER,
                    units_to=MILLIGRAMS_PER_DECILITER,
                    mw=MW_CREATININE,  # g/mol
                ),
                2,
            ),
            1.21,
        )

    def test_egfr_ckd_epi_2009_calculator(self):
        # raises on invalid gender
        self.assertRaises(
            EgfrCalculatorError,
            EgfrCkdEpi2009,
            gender="blah",
            age_in_years=30,
            creatinine_value=1.0,
            creatinine_units=MILLIGRAMS_PER_DECILITER,
            ethnicity=BLACK,
        )

        # raises on low age
        self.assertRaises(
            EgfrCalculatorError,
            EgfrCkdEpi2009,
            gender=FEMALE,
            age_in_years=3,
            creatinine_value=1.0,
            creatinine_units=MILLIGRAMS_PER_DECILITER,
            ethnicity=BLACK,
        )

        self.assertRaises(
            EgfrCalculatorError,
            EgfrCkdEpi2009,
            gender=FEMALE,
            age_in_years=30,
            ethnicity=BLACK,
        )

        egfr = EgfrCkdEpi2009(
            gender=FEMALE,
            age_in_years=30,
            creatinine_value=52.0,
            creatinine_units=MICROMOLES_PER_LITER,
            ethnicity=BLACK,
        )
        self.assertEqual(0.7, egfr.kappa)

        egfr = EgfrCkdEpi2009(
            gender=MALE,
            age_in_years=30,
            creatinine_value=52.0,
            creatinine_units=MICROMOLES_PER_LITER,
            ethnicity=BLACK,
        )
        self.assertEqual(0.9, egfr.kappa)

        egfr = EgfrCkdEpi2009(
            gender=FEMALE,
            age_in_years=30,
            creatinine_value=53.0,
            creatinine_units=MICROMOLES_PER_LITER,
            ethnicity=BLACK,
        )
        self.assertEqual(-0.329, egfr.alpha)

        egfr = EgfrCkdEpi2009(
            gender=MALE,
            age_in_years=30,
            creatinine_value=53.0,
            creatinine_units=MICROMOLES_PER_LITER,
            ethnicity=BLACK,
        )
        self.assertEqual(-0.411, egfr.alpha)

        egfr1 = EgfrCkdEpi2009(
            gender=MALE,
            ethnicity=BLACK,
            creatinine_value=53.0,
            age_in_years=30,
            creatinine_units=MICROMOLES_PER_LITER,
        )
        self.assertEqual(round_half_away_from_zero(egfr1.value, 2), 156.42)

        egfr2 = EgfrCkdEpi2009(
            gender=FEMALE,
            ethnicity=BLACK,
            creatinine_value=53.0,
            age_in_years=30,
            creatinine_units=MICROMOLES_PER_LITER,
        )
        self.assertEqual(round_half_away_from_zero(egfr2.value, 3), 141.799)

        egfr1 = EgfrCkdEpi2009(
            gender=MALE,
            ethnicity=NON_BLACK,
            creatinine_value=53.0,
            age_in_years=30,
            creatinine_units=MICROMOLES_PER_LITER,
        )
        self.assertEqual(round_half_away_from_zero(egfr1.value, 2), 134.96)

        egfr2 = EgfrCkdEpi2009(
            gender=FEMALE,
            ethnicity=NON_BLACK,
            creatinine_value=53.0,
            age_in_years=30,
            creatinine_units=MICROMOLES_PER_LITER,
        )
        self.assertEqual(round_half_away_from_zero(egfr2.value, 2), 122.35)

        egfr3 = EgfrCkdEpi2009(
            gender=MALE,
            ethnicity=BLACK,
            creatinine_value=150.8,
            age_in_years=60,
            creatinine_units=MICROMOLES_PER_LITER,
        )
        self.assertEqual(round_half_away_from_zero(egfr3.value, 4), 49.4921)

        egfr4 = EgfrCkdEpi2009(
            gender=MALE,
            ethnicity=BLACK,
            creatinine_value=152.0,
            age_in_years=60,
            creatinine_units=MICROMOLES_PER_LITER,
        )
        self.assertEqual(round_half_away_from_zero(egfr4.value, 4), 49.0192)

        egfr4 = EgfrCkdEpi2009(
            gender=MALE,
            ethnicity=BLACK,
            creatinine_value=152.0,
            age_in_years=59,
            creatinine_units=MICROMOLES_PER_LITER,
        )
        self.assertEqual(round_half_away_from_zero(egfr4.value, 4), 49.3647)

        egfr = EgfrCkdEpi2009(
            gender=FEMALE,
            ethnicity=BLACK,
            creatinine_value=150.8,
            age_in_years=60,
            creatinine_units=MICROMOLES_PER_LITER,
        )
        self.assertEqual(round_half_away_from_zero(egfr.value, 4), 37.1816)

        egfr = EgfrCkdEpi2009(
            gender=FEMALE,
            ethnicity=BLACK,
            creatinine_value=152.0,
            age_in_years=60,
            creatinine_units=MICROMOLES_PER_LITER,
        )
        self.assertEqual(round_half_away_from_zero(egfr.value, 4), 36.8263)

    def test_egfr_ckd_epi2021(self):
        egfr = EgfrCkdEpi2021(
            gender=FEMALE,
            age_in_years=30,
            creatinine_value=52.0,
            creatinine_units=MICROMOLES_PER_LITER,
            ethnicity=BLACK,
        )
        self.assertEqual(0.7, egfr.kappa)

        egfr = EgfrCkdEpi2021(
            gender=MALE,
            age_in_years=30,
            creatinine_value=52.0,
            creatinine_units=MICROMOLES_PER_LITER,
            ethnicity=BLACK,
        )
        self.assertEqual(0.9, egfr.kappa)

        egfr = EgfrCkdEpi2021(
            gender=FEMALE,
            age_in_years=30,
            creatinine_value=53.0,
            creatinine_units=MICROMOLES_PER_LITER,
            ethnicity=BLACK,
        )
        self.assertEqual(-0.241, egfr.alpha)
        self.assertEqual(1.012, egfr.gender_factor)
        self.assertEqual(0.7, egfr.kappa)
        self.assertEqual(0.81, round(egfr.age_factor, 4))
        self.assertEqual(120.83, round(egfr.value, 2))

        egfr = EgfrCkdEpi2021(
            gender=MALE,
            age_in_years=30,
            creatinine_value=53.0,
            creatinine_units=MICROMOLES_PER_LITER,
            ethnicity=BLACK,
        )
        self.assertEqual(-0.302, egfr.alpha)
        self.assertEqual(1, egfr.gender_factor)
        self.assertEqual(0.9, egfr.kappa)
        self.assertEqual(0.81, round(egfr.age_factor, 4))
        self.assertEqual(130.03, round(egfr.value, 2))

        egfr1 = EgfrCkdEpi2021(
            gender=MALE,
            ethnicity=BLACK,
            creatinine_value=0.600,
            age_in_years=30,
            creatinine_units=MILLIGRAMS_PER_DECILITER,
        )
        self.assertEqual(round_half_away_from_zero(egfr1.value, 1), 130.0)

    def test_egfr_cockcroft_gault_calculator(self):
        # raises on invalid gender
        self.assertRaises(
            EgfrCalculatorError,
            EgfrCockcroftGault,
            gender="blah",
            age_in_years=30,
            creatinine_value=1.0,
            creatinine_units=MICROMOLES_PER_LITER,
        )
        # raises on low age
        self.assertRaises(
            EgfrCalculatorError,
            EgfrCockcroftGault,
            gender=FEMALE,
            age_in_years=3,
            creatinine_value=1.0,
            creatinine_units=MICROMOLES_PER_LITER,
            weight=65.0,
        )

        # raises on missing weight
        egfr = EgfrCockcroftGault(
            gender=FEMALE,
            age_in_years=30,
            creatinine_value=1.0,
            creatinine_units=MICROMOLES_PER_LITER,
        )
        self.assertRaises(EgfrCalculatorError, getattr, egfr, "value")

        egfr = EgfrCockcroftGault(
            gender=MALE,
            age_in_years=30,
            creatinine_value=50.0,
            creatinine_units=MICROMOLES_PER_LITER,
            weight=65.0,
        )
        self.assertEqual(round_half_away_from_zero(egfr.value, 2), 175.89)

        egfr = EgfrCockcroftGault(
            gender=MALE,
            age_in_years=30,
            creatinine_value=50.8,
            creatinine_units=MICROMOLES_PER_LITER,
            weight=65.0,
        )
        self.assertEqual(round_half_away_from_zero(egfr.value, 2), 173.12)

        egfr = EgfrCockcroftGault(
            gender=MALE,
            age_in_years=30,
            creatinine_value=50.9,
            creatinine_units=MICROMOLES_PER_LITER,
            weight=65.0,
        )
        self.assertEqual(round_half_away_from_zero(egfr.value, 2), 172.78)

        egfr = EgfrCockcroftGault(
            gender=FEMALE,
            age_in_years=30,
            creatinine_value=50.9,
            creatinine_units=MICROMOLES_PER_LITER,
            weight=65.0,
        )
        self.assertEqual(round_half_away_from_zero(egfr.value, 2), 147.5)

        egfr = EgfrCockcroftGault(
            gender=FEMALE,
            creatinine_value=1.3,
            age_in_years=30,
            creatinine_units=MILLIGRAMS_PER_DECILITER,
            weight=65.0,
        )

        self.assertEqual(round_half_away_from_zero(egfr.value, 2), 65.33)

    def test_egfr_cockcroft_gault_calculator2(self):
        egfr2 = EgfrCockcroftGault(
            gender=MALE,
            creatinine_value=0.9,
            age_in_years=30,
            creatinine_units=MILLIGRAMS_PER_DECILITER,
            weight=65.0,
        )

        self.assertEqual(round_half_away_from_zero(egfr2.value, 2), 110.54)

    def test_egfr_percent_change(self):
        self.assertGreater(egfr_percent_change(51.10, 131.50), 20.0)
        self.assertLess(egfr_percent_change(51.10, 61.10), 20.0)
        self.assertEqual(egfr_percent_change(51.10, 51.10), 0.0)
        self.assertLess(egfr_percent_change(51.10, 21.10), 20.0)
        self.assertEqual(egfr_percent_change(51.10, 0), 0.0)
