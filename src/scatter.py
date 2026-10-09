"""
import matplotlib.pyplot as plt
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')

data_file = sys.argv[1]
out_file = sys.argv[2]
title = sys.argv[3]
x = sys.argv[4]
y = sys.argv[5]

X = []
Y = []
for l in open(data_file):
    A = l.rstrip().split()
    X.append(float(A[0]))
    Y.append(float(A[1]))

fig, ax = plt.subplots()
ax.scatter(X, Y)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_xlabel(x)
ax.set_ylabel(y)
ax.set_title(title)

plt.savefig(out_file, bbox_inches='tight')
"""
import fire_gdp
import argparse
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("Agg")


def make_scatter(co2_file, gdp_file, country, output_file):
    """Create a scatter plot of GDP versus forest fire emissions."""

    data = fire_gdp.get_fire_gdp_year_data(
        co2_file, gdp_file, country
    )

    if not data:
        print(f"No matching data found for {country}.")
        return False

    gdp = []
    fires = []

#    for row in data:
    if country == "Finland":
        gdp = [row[2] / 1000 for row in data]
        gdp_unit = "billions"
    else:
        gdp = [row[2] for row in data]
        gdp_unit = "10 millions"

    fires = [row[1] for row in data]
    fig, ax = plt.subplots()
    # ax.scatter(fires, gdp)
    ax.set_ylabel("Forest fire emissions")
    ax.set_xlabel(f"GDP ({gdp_unit} of local currency)")
    ax.ticklabel_format(style="plain", axis="y")
    # fires.append(row[1])

    ax.scatter(gdp, fires)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # ax.set_xlabel("GDP (millions of local currency)")
    # ax.set_ylabel("Forest fire emissions")
    ax.set_title(f"Forest Fire Emissions vs GDP: {country}")

    fig.savefig(output_file, bbox_inches="tight")
    plt.close(fig)

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Plot forest fire emissions against GDP."
    )

    parser.add_argument("--co2_file", required=True)
    parser.add_argument("--gdp_file", required=True)
    parser.add_argument("--country", required=True)
    parser.add_argument("--output_file", required=True)

    args = parser.parse_args()

    success = make_scatter(
        args.co2_file,
        args.gdp_file,
        args.country,
        args.output_file
    )

    if not success:
        parser.exit(1, "Plot was not created.\n")


if __name__ == "__main__":
    main()
