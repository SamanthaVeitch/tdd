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


class TestGetColumnIndex(unittest.TestCase):

    def test_name_present(self):
        pass


if __name__ == '__main__':
    unittest.main()
