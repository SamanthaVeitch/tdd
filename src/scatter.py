import fire_gdp

import argparse
import matplotlib
import matplotlib.pyplot as plt
# Use a non-interactive backend to save plots without opening a window.
matplotlib.use("Agg")


# Input GDP values are in millions of local currency.
GDP_DIVISORS = {
    "millions": 1,
    "billions": 1_000,
    "trillions": 1_000_000,
}


def make_scatter(
    co2_file, gdp_file, country, output_file, gdp_unit="millions"
):
    """
    Create a scatter plot of forest fire emissions against GDP.

    GDP values are read in millions of local currency and converted
    to the selected display unit.

    Parameters
    ----------
    co2_file : str
        Path to the CSV file containing forest fire emissions.
    gdp_file : str
        Path to the CSV file containing GDP data.
    country : str
        Country name as it appears in both CSV files.
    output_file : str
        Path where the scatter plot will be saved. The parent
        directory must already exist.
    gdp_unit : str, optional
        Unit used to display GDP. Must be "millions", "billions",
        or "trillions". Defaults to "millions".

    Returns
    -------
    bool
        True if the plot was created successfully.
        False if no matching data was found.
    """
    data = fire_gdp.get_fire_gdp_year_data(
        co2_file, gdp_file, country
    )

    if not data:
        print(f"No matching data found for {country}.")
        return False

    divisor = GDP_DIVISORS[gdp_unit]

    gdp = [row[2] / divisor for row in data]
    fires = [row[1] for row in data]

    fig, ax = plt.subplots()

    ax.scatter(gdp, fires)

    ax.set_xlabel(f"GDP ({gdp_unit} of local currency)")
    ax.set_ylabel("Forest fire emissions")
    ax.set_title(f"Forest Fire Emissions vs GDP: {country}")

    ax.ticklabel_format(style="plain", axis="y")

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.savefig(output_file, bbox_inches="tight")
    plt.close(fig)

    return True


def main():
    """
    Parse command-line arguments and generate a scatter plot.

    The command-line interface requires paths to the emissions
    and GDP datasets, a country name, and an output file path.
    GDP display units are optional and default to millions.

    Returns
    -------
    None
        The function does not return a value.

    Raises
    ------
    SystemExit
        If required arguments are missing or plot creation fails.
    """
    parser = argparse.ArgumentParser(
        description="Plot forest fire emissions against GDP."
    )

    parser.add_argument("--co2_file", required=True)
    parser.add_argument("--gdp_file", required=True)
    parser.add_argument("--country", required=True)
    parser.add_argument("--output_file", required=True)

    parser.add_argument(
        "--gdp_unit",
        choices=GDP_DIVISORS.keys(),
        default="millions",
        help="GDP display unit (default: millions).",
    )

    args = parser.parse_args()

    success = make_scatter(
        args.co2_file,
        args.gdp_file,
        args.country,
        args.output_file,
        args.gdp_unit,
    )

    if not success:
        parser.exit(1, "Plot was not created.\n")


if __name__ == "__main__":
    main()
