import csv
import os
import sys
import unittest
import fire_gdp


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


class TestGetColumnIndex(unittest.TestCase):

    def test_name_present(self):
        pass


if __name__ == '__main__':
    unittest.main()
