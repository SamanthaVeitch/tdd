
rule all:
    input:
        "plots/finland.png",
        "plots/madagascar.png",
        "plots/usa.png"


rule finland:
    input:
        co2="data/Agrofood_co2_emission.csv",
        gdp="data/IMF_GDP.csv"
    output:
        "plots/finland.png"
    shell:
        "python src/scatter.py "
        "--co2_file {input.co2} "
        "--gdp_file {input.gdp} "
        "--country Finland "
        "--output_file {output}"


rule madagascar:
    input:
        co2="data/Agrofood_co2_emission.csv",
        gdp="data/IMF_GDP.csv"
    output:
        "plots/madagascar.png"
    shell:
        "python src/scatter.py "
        "--co2_file {input.co2} "
        "--gdp_file {input.gdp} "
        "--country Madagascar "
        "--output_file {output}"


rule usa:
    input:
        co2="data/Agrofood_co2_emission.csv",
        gdp="data/IMF_GDP.csv"
    output:
        "plots/usa.png"
    shell:
        "python src/scatter.py "
        "--co2_file {input.co2} "
        "--gdp_file {input.gdp} "
        '--country "United States of America" '
        "--output_file {output}"
