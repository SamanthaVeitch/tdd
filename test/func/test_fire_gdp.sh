test -e test/func/ssshtest || exit 1
. test/func/ssshtest

# Example of the pattern to follow. Replace with tests for your own scripts.
#
# run test_plot_runs python src/plot_fire_gdp.py --out fire_gdp.png
# assert_exit_code 0
# assert_equal fire_gdp.png $( ls fire_gdp.png )
