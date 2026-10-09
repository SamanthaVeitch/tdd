import csv


def get_data(file_name,
             query_column=None,
             query_value=None,
             return_header=False):
    with open(file_name, "r", newline="") as file:
        reader = csv.reader(file)
        header = next(reader)
        rows = list(reader)

    if query_column is not None and query_value is not None:
        rows = [
            row for row in rows
            if row[query_column] == query_value
        ]

    if return_header:
        rows.insert(0, header)

    return rows


def get_column_index(header, column_name):
    return header.index(column_name)


def get_fire_gdp_year_data(co2_file, gdp_file, country):
    pass
