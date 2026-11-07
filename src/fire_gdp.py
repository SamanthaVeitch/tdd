import csv
import warnings

CO2_REQUIRED_COLUMNS = ("Area", "Year", "Forest fires")
GDP_REQUIRED_COLUMNS = ("Country",)


def get_data(file_name,
             query_column=None,
             query_value=None,
             return_header=False):
    """
    Read a CSV file and return its contents as a list of rows.
    """
    with open(file_name, "r", newline="") as file:
        reader = csv.reader(file)
        header = next(reader, None)
        if header is None:
            raise ValueError(f"{file_name}: CSV file is empty.")
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
    """
    Get the index of a column in a CSV with header.
    """
    try:
        return header.index(column_name)
    except ValueError:
        return None


def get_fire_gdp_year_data(co2_file, gdp_file, country):
    """
    Match forest fire emissions and GDP data by country and year.
    Missing values are skipped with a warning.

    Parameters
    ----------
    co2_file : str
        Path to the CSV file containing forest fire emissions.
    gdp_file : str
        Path to the CSV file containing GDP values in millions
        of local currency.
    country : str
        Country name as it appears in both CSV files.

    Returns
    -------
    list
        Records containing [year, forest fire emissions, GDP].
        Year is an integer; emissions and GDP are floats.
        Returns an empty list if no matching records exist.

    Raises
    ------
    ValueError
        If required columns are missing or a CSV file is empty.
    OSError
        If an input file cannot be opened or read.

    Warns
    -----
    UserWarning
        If an observation has a missing year, forest fire
        emissions value, or GDP value. The affected record
        is skipped.
    """
    co2_data = get_data(
        co2_file,
        query_column=0,
        query_value=country,
        return_header=True,
    )
    gdp_data = get_data(
        gdp_file,
        query_column=0,
        query_value=country,
        return_header=True,
    )

    co2_header = co2_data[0]
    gdp_header = gdp_data[0]

    validate_required_columns(
        co2_header, CO2_REQUIRED_COLUMNS, co2_file
    )

    validate_required_columns(
        gdp_header, GDP_REQUIRED_COLUMNS, gdp_file
    )

    if not gdp_header or not gdp_header[0].strip():
        raise ValueError(
            f"{gdp_file}: Missing required country column."
        )

    if len(gdp_header) < 2:
        raise ValueError(
            f"{gdp_file}: Missing GDP year columns."
        )

    if len(co2_data) < 2 or len(gdp_data) < 2:
        return []

    year_index = get_column_index(co2_header, "Year")
    fires_index = get_column_index(co2_header, "Forest fires")

    gdp_row = gdp_data[1]
    results = []

    for co2_row in co2_data[1:]:
        if year_index >= len(co2_row):
            warnings.warn(
                f"{co2_file}, {country}: Missing 'Year' value. "
                "Skipping record.",
                UserWarning,
                stacklevel=2,
            )
            continue

        year = co2_row[year_index].strip()

        try:
            year_number = int(year)
        except ValueError:
            warnings.warn(
                f"{co2_file}, {country}: Invalid year '{year}'. "
                "Skipping record.",
                UserWarning,
                stacklevel=2,
            )
            continue

        gdp_index = get_column_index(gdp_header, year)

        if gdp_index is None:
            continue

        if fires_index >= len(co2_row):
            fire_value = ""
        else:
            fire_value = co2_row[fires_index].strip()

        if gdp_index >= len(gdp_row):
            gdp_value = ""
        else:
            gdp_value = gdp_row[gdp_index].strip()

        if not fire_value:
            warnings.warn(
                f"{co2_file}, {country}, year {year}: "
                "Missing 'Forest fires' value. Skipping record.",
                UserWarning,
                stacklevel=2,
            )
            continue

        if not gdp_value:
            warnings.warn(
                f"{gdp_file}, {country}, year {year}: "
                "Missing GDP value. Skipping record.",
                UserWarning,
                stacklevel=2,
            )
            continue

        results.append([
            year_number,
            float(fire_value),
            float(gdp_value),
        ])

    return results


def validate_required_columns(header, required_columns, file_name):
    """
    Validate that a CSV header contains every required column.

    Parameters
    ----------
    header : list
        Column names from the CSV header.
    required_columns : tuple
        Names of columns required for processing.
    file_name : str
        Path to the CSV file being validated.

    Raises
    ------
    ValueError
        If one or more required columns are missing.
    """
    missing_columns = [
        column for column in required_columns
        if column not in header
    ]

    if missing_columns:
        missing = ", ".join(missing_columns)
        raise ValueError(
            f"{file_name}: Missing required columns: {missing}"
        )
