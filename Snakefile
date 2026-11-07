
COUNTRIES = [
    "Finland",
    "Madagascar",
    "United States of America",
    "Canada",
    "France",
    "Germany",
]

COUNTRY_FILES = [
    "finland",
    "madagascar",
    "usa",
    "canada",
    "france",
    "germany",
]



rule all:
    input:
        expand("plots/{country}.png", country=COUNTRY_FILES)


rule scatter_plot:
    input:
        co2="data/Agrofood_co2_emission.csv",
        gdp="data/IMF_GDP.csv"
    output:
        "plots/{country}.png"
    params:
        country=lambda wildcards: COUNTRIES[
            COUNTRY_FILES.index(wildcards.country)
        ]
    shell:
        "python src/scatter.py "
        "--co2_file {input.co2} "
        "--gdp_file {input.gdp} "
        '--country "{params.country}" '
        "--output_file {output}"
