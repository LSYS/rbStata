from wbStata.cli import normalize_dta_filename
from wbStata.cli import convert_dta
from wbStata.cli import add_suffix
from wbStata.cli import get_output_name
from wbStata.cli import normalize_filename
from click.testing import CliRunner
from wbStata.cli import wbstata

def test_normalize_dta_filename():
    expected = "census.dta"

    filename = "census"
    result = normalize_dta_filename(filename)
    assert result == expected

    filename = "census.dta"
    result = normalize_dta_filename(filename)
    assert result == expected

    expected = "datasets/census.dta"

    filename = "datasets/census"
    result = normalize_dta_filename(filename)
    assert result == expected

    filename = "datasets/census.dta"
    result = normalize_dta_filename(filename)
    assert result == expected


def test_normalize_filename():
    expected = "census.dta"
    result = normalize_filename("Census.dta")
    assert expected == result

    result = normalize_filename("Cens  us.dta")
    assert expected == result


def test_convert_dta():
    for version in range(10, 17 + 1):
        convert_dta("datasets/census.dta", "temp/test-output.dta", version=version)


def test_add_suffix():
    expected = "census-v13.dta"
    result = add_suffix("census.dta", suffix="-v13")
    assert result == expected

    expected = "dir/census-v13.dta"
    result = add_suffix("dir/census.dta", suffix="-v13")
    assert result == expected


def test_get_output_name():
    file = "census.dta"

    # Overwriting
    expected = file
    result = get_output_name(file, version=13, overwrite=True)
    assert result == expected

    # Using output option
    output = "output.dta"
    expected = output
    result = get_output_name(file, version=13, overwrite=False, output=output)
    assert result == expected

    # Using suffix
    suffix = "-v13"
    expected = add_suffix(file, suffix)
    result = get_output_name(file, version=13, overwrite=False, suffix=suffix)
    assert result == expected

    # Using default
    version = 13
    suffix = "-v13"
    expected = add_suffix(file, suffix)
    result = get_output_name(file, version=version, overwrite=False)
    assert result == expected


import click
def test_wbstata():
    runner = CliRunner()

    # Check that prompt works with just file (prompt for version)
    result = runner.invoke(wbstata, ['datasets/census.dta'])
    assert result.exit_code==0
    assert result.output=="Which version to convert to? [13]: \n"

    # Check minimal command
    dta = "datasets2/census.dta"
    expected_output = f"Done writing {dta} to datasets2/census-v13.dta in version 13.\n"
    result = runner.invoke(wbstata, [f'{dta}', '--version', '13', '--verbose'])
    assert result.exit_code==0
    assert result.output==expected_output

    # Check multiple
    dta1 = "datasets2/census.dta"
    dta2 = "datasets2/auto.dta"
    dta3 = "datasets2/lifeexp.dta"
    result = runner.invoke(wbstata, [f'{dta1}', f'{dta2}', f'{dta3}', '--version', '13', '--verbose'])
    assert result.exit_code==0
    assert f"Done writing {dta1}" in result.output
    assert f"Done writing {dta2}" in result.output
    assert f"Done writing {dta3}" in result.output
    assert f"in version 13." in result.output

    # dta = "datasets2/census.dta"
    # expected_output = f"Done overwriting {dta} as version 13."
    # result = runner.invoke(wbstata, [f'{dta}', '--version', '13', '--verbose', '--overwrite'])
    # assert result.output==expected_output

    # Check that error is caught when file does not exist


    # dta = "datasets2/census.dta"
    # expected_output = f"Done overwriting {dta} as version 13."
    # result = runner.invoke(wbstata, [f'{dta}', '--version', '13', '--verbose', '--overwrite'])
    # assert result.output==expected_output
    # Check that prompt works with just wbstata



    # Check that verbose works

    # # Check that error is caught when file does not exist
    # result = runner.invoke(wbstata, ['datasets/census.dta'])
    # assert result.exit_code==0
    # assert result.output=="Which version to convert to? [13]: \n"
