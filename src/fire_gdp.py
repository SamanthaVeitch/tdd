import csv


def get_data(file_name,
             query_column=None,
             query_value=None,
             return_header=False):
    with open(file_name, "r", newline="") as file:
        reader = csv.reader(file)
        next(reader)
        rows = list(reader)

    if query_column is not None and query_value is not None:
        rows = [
            row for row in rows
            if row[query_column] == query_value
        ]

    return rows


def get_column_index(header, column_name):
    pass


def get_fire_gdp_year_data(co2_file, gdp_file, country):
    pass
