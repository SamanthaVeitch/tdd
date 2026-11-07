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
        GDP display unit: "millions", "billions", or "trillions".
        Defaults to "millions".

    Returns
    -------
    bool
        True if the plot was saved successfully.
        False if no matching data was found.
    """
    data = fire_gdp.get_fire_gdp_year_data(
        co2_file, gdp_file, country
    )

    if not data:
        return False

    divisor = GDP_DIVISORS[gdp_unit]
    gdp = [row[2] / divisor for row in data]
    fires = [row[1] for row in data]

    fig, ax = plt.subplots()

    try:
        ax.scatter(gdp, fires)

        ax.set_xlabel(f"GDP ({gdp_unit} of local currency)")
        ax.set_ylabel("Forest fire emissions")
        ax.set_title(f"Forest Fire Emissions vs GDP: {country}")

        ax.ticklabel_format(style="plain", axis="y")

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        fig.savefig(output_file, bbox_inches="tight")
    finally:
        # Release the figure even if saving raises an exception.
        plt.close(fig)

    return True


def main():
    """
    Parse command-line arguments and generate a scatter plot.

    Required arguments identify the emissions dataset, GDP
    dataset, country, and output file. The GDP display unit
    defaults to millions.

    Returns
    -------
    None
        The function does not return a value on success.

    Raises
    ------
    SystemExit
        If arguments are invalid, file operations fail, or
        no matching data is found.
    """
    parser = argparse.ArgumentParser(
        description="Plot forest fire emissions against GDP."
    )

    parser.add_argument(
        "--co2_file",
        required=True,
        help="Path to the CSV file containing forest fire emissions.",
    )
    parser.add_argument(
        "--gdp_file",
        required=True,
        help="Path to the CSV file containing GDP data.",
    )
    parser.add_argument(
        "--country",
        required=True,
        help="Country name exactly as it appears in both CSV files.",
    )
    parser.add_argument(
        "--output_file",
        required=True,
        help="Output image path; the parent directory must exist.",
    )
    parser.add_argument(
        "--gdp_unit",
        choices=GDP_DIVISORS.keys(),
        default="millions",
        help="GDP display unit (default: millions).",
    )

    args = parser.parse_args()

    try:
        success = make_scatter(
            args.co2_file,
            args.gdp_file,
            args.country,
            args.output_file,
            args.gdp_unit,
        )
    except (OSError, ValueError) as error:
        parser.exit(1, f"Error: {error}\n")

    if not success:
        parser.exit(
            1,
            f"No matching data found for {args.country}. "
            "Plot was not created.\n",
        )


if __name__ == "__main__":
    main()
