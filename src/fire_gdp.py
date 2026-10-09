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
    try:
        return header.index(column_name)
    except ValueError:
        return None


def get_fire_gdp_year_data(co2_file, gdp_file, country):
    co2_data = get_data(
        co2_file, query_column=0,
        query_value=country, return_header=True
    )

    gdp_data = get_data(
        gdp_file, query_column=0,
        query_value=country, return_header=True
    )

    co2_header = co2_data[0]
    gdp_header = gdp_data[0]

    fires_index = get_column_index(co2_header, "Forest fires")

    gdp_row = gdp_data[1]
    results = []

    for co2_row in co2_data[1:]:
        year = co2_row[1]
        gdp_index = get_column_index(gdp_header, year)

        if gdp_index is None:
            continue

        fire_value = co2_row[fires_index]
        gdp_value = gdp_row[gdp_index]

        if fire_value == "" or gdp_value == "":
            continue

        results.append([
            int(year),
            float(fire_value),
            float(gdp_value)
        ])

    return results
