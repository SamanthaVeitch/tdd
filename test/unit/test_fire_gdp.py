import csv
import os
import sys
import unittest

from src import fire_gdp


class TestGetData(unittest.TestCase):

    def test_get_data_no_query(self):
        file_name = os.path.join(
            "test", "data", "test_Agrofood_co2_emission.csv"
        )

        with open(file_name, "r", newline="") as file:
            reader = csv.reader(file)
            next(reader)
            expected = list(reader)

        result = fire_gdp.get_data(file_name)

        self.assertEqual(result, expected)

    def test_get_data_query(self):
        file_name = os.path.join(
            "test", "data", "test_Agrofood_co2_emission.csv"
        )

        with open(file_name, "r", newline="") as file:
            reader = csv.reader(file)
            next(reader)
            expected = [
                row for row in reader if row[0] == "Finland"
            ]

        result = fire_gdp.get_data(
            file_name, query_column=0, query_value="Finland"
        )

        self.assertEqual(result, expected)

    def test_get_data_return_header(self):
        file_name = os.path.join(
            "test", "data", "test_Agrofood_co2_emission.csv"
        )

        with open(file_name, "r", newline="") as file:
            reader = csv.reader(file)
            expected = list(reader)

        result = fire_gdp.get_data(
            file_name, return_header=True
        )

        self.assertEqual(result, expected)

    def test_get_data_query_no_match_with_header(self):
        file_name = os.path.join(
            "test", "data", "test_Agrofood_co2_emission.csv"
        )

        with open(file_name, "r", newline="") as file:
            header = next(csv.reader(file))

        result = fire_gdp.get_data(
            file_name,
            query_column=0,
            query_value="NonexistentCountry",
            return_header=True
        )

        self.assertEqual(result, [header])

    def test_get_data_query_with_header(self):
        file_name = os.path.join(
            "test", "data", "test_Agrofood_co2_emission.csv"
        )

        with open(file_name, "r", newline="") as file:
            reader = csv.reader(file)
            header = next(reader)
            expected = [header]

            for row in reader:
                if row[0] == "Finland":
                    expected.append(row)

        result = fire_gdp.get_data(
            file_name,
            query_column=0,
            query_value="Finland",
            return_header=True
        )

        self.assertEqual(result, expected)


class TestGetColumnIndex(unittest.TestCase):
    def test_get_column_index_present(self):
        header = ["Area", "Year", "Forest fires"]

        result = fire_gdp.get_column_index(
            header, "Forest fires"
        )

        self.assertEqual(result, 2)

    def test_get_column_index_missing(self):
        header = ["Area", "Year", "Forest fires"]

        result = fire_gdp.get_column_index(
            header, "GDP"
        )

        self.assertIsNone(result)

    def test_get_column_index_empty_header(self):
        header = []

        result = fire_gdp.get_column_index(
            header, "Forest fires"
        )

        self.assertIsNone(result)


class TestGetFireGDPYearData(unittest.TestCase):

    def test_get_fire_gdp_finland(self):
        co2_file = os.path.join(
            "test", "data", "test_Agrofood_co2_emission.csv"
        )
        gdp_file = os.path.join(
            "test", "data", "test_IMF_GDP.csv"
        )

        result = fire_gdp.get_fire_gdp_year_data(
            co2_file, gdp_file, "Finland"
        )

        self.assertEqual(result[0][0], 1990)
        self.assertIsInstance(result[0][0], int)
        self.assertIsInstance(result[0][1], float)
        self.assertIsInstance(result[0][2], float)

    def test_get_fire_gdp_multiple_years(self):
        co2_file = os.path.join(
            "test", "data", "test_Agrofood_co2_emission.csv"
        )
        gdp_file = os.path.join(
            "test", "data", "test_IMF_GDP.csv"
        )

        result = fire_gdp.get_fire_gdp_year_data(
            co2_file, gdp_file, "Finland"
        )

        self.assertEqual(len(result), 29)

        self.assertEqual(result[0], [1990, 0.6875, 90959.0])
        self.assertEqual(result[1], [1991, 0.6875, 86899.0])
        self.assertEqual(result[2], [1992, 0.6875, 84782.0])

    def test_get_fire_gdp_missing_gdp(self):
        co2_file = os.path.join(
            "test", "data", "test_Agrofood_co2_emission.csv"
        )
        gdp_file = os.path.join(
            "test", "data", "test_IMF_GDP.csv"
        )

        result = fire_gdp.get_fire_gdp_year_data(
            co2_file, gdp_file, "Madagascar"
        )

        self.assertEqual(len(result), 14)
        self.assertEqual(result[0], [2007, 415.5537, 15974090.0])
        self.assertEqual(result[-1], [2020, 586.4382, 49435649.38])

    def test_get_fire_gdp_missing_fires(self):
        co2_file = os.path.join(
            "test", "data", "test_Agrofood_co2_emission.csv"
        )
        gdp_file = os.path.join(
            "test", "data", "test_IMF_GDP.csv"
        )

        result = fire_gdp.get_fire_gdp_year_data(
            co2_file, gdp_file, "Finland"
        )

        years = [row[0] for row in result]

        self.assertNotIn(2004, years)
        self.assertEqual(len(result), 29)

    def test_get_fire_gdp_missing_year(self):
        co2_file = os.path.join(
            "test", "data", "test_Agrofood_co2_emission.csv"
        )
        gdp_file = os.path.join(
            "test", "data", "test_IMF_GDP.csv"
        )

        result = fire_gdp.get_fire_gdp_year_data(
            co2_file, gdp_file, "Finland"
        )

        years = [row[0] for row in result]

        self.assertNotIn(2021, years)
        self.assertEqual(len(result), 29)


if __name__ == '__main__':
    unittest.main()
