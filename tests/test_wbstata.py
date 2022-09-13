from wbStata.cli import normalize_dta_filename
from wbStata.cli import convert_dta
from wbStata.cli import add_suffix
from wbStata.cli import get_output_name
from wbStata.cli import normalize_filename
from wbStata.cli import is_dta_file
from wbStata.cli import glob_dta_files
from click.testing import CliRunner
from wbStata.cli import wbstata
import pytest
from click import ClickException


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
    result = get_output_name(file, target_version=13, overwrite=True)
    assert result == expected

    # Using output option
    output = "output.dta"
    expected = output
    result = get_output_name(file, target_version=13, overwrite=False, output=output)
    assert result == expected

    # Using suffix
    suffix = "-v13"
    expected = add_suffix(file, suffix)
    result = get_output_name(file, target_version=13, overwrite=False, suffix=suffix)
    assert result == expected

    # Using default
    version = 13
    suffix = "-v13"
    expected = add_suffix(file, suffix)
    result = get_output_name(file, target_version=version, overwrite=False)
    assert result == expected


def test_is_dta_file():
    valid_file = "datasets/census.dta"
    is_dta_file(valid_file)

    invalid_file = "wrongfile.dta"
    with pytest.raises(ClickException) as excinfo:
        is_dta_file(invalid_file)
    assert f"{invalid_file} is not a valid path to a dta file." in str(excinfo)

    invalid_file = "census"
    with pytest.raises(ClickException) as excinfo:
        is_dta_file(invalid_file)
    assert f"{invalid_file} is not a valid path to a dta file." in str(excinfo)


def test_glob_dta_files():
    files = glob_dta_files(recursive=False)
    assert len(files) == 0

    files = glob_dta_files(recursive=True)
    assert len(files) > 0


def test_convert_dta():
    for version in range(10, 17 + 1):
        convert_dta(
            "datasets/census.dta", "datasets/test-output.dta", target_version=version
        )


def test_wbstata():
    runner = CliRunner()

    COMPLETION_MSG = "Conversions complete."

    # Check that prompt works
    result = runner.invoke(wbstata)
    assert result.exit_code == 0
    assert "> .dta file(s)" in result.output
    assert (
        "Welcome to the wbStata quickstart command-line utility."
        in result.output
    )
    assert "You will be prompted for relevant settings." in result.output
    assert "Please enter values under the following settings." in result.output
    assert (
        "(just press Enter to accept the default value in brackets)"
        in result.output
    )

    # Check that prompt works with just file (prompt for version)
    result = runner.invoke(wbstata, ["datasets/census.dta"])
    assert result.exit_code == 0
    assert "> Target version" in result.output

    # Check minimal command
    dta = "datasets2/census.dta"
    expected_output = (
        f"{dta} to datasets2/census-v13.dta in version 13.\n"
    )
    result = runner.invoke(wbstata, [f"{dta}", "--target-version", "13", "--verbose"])
    assert result.exit_code == 0
    assert expected_output in result.output
    assert COMPLETION_MSG in result.output

    # Check multiple
    dta1 = "datasets2/census.dta"
    dta2 = "datasets2/auto.dta"
    dta3 = "datasets2/lifeexp.dta"
    result = runner.invoke(
        wbstata,
        [f"{dta1}", f"{dta2}", f"{dta3}", "--target-version", "13", "--verbose"],
    )
    assert result.exit_code == 0
    assert f"{dta1}" in result.output
    assert f"{dta2}" in result.output
    assert f"{dta3}" in result.output
    assert "in version 13." in result.output
    assert COMPLETION_MSG in result.output

    # Check that error is caught when file does not exist
    invalid_file = "dummy.dta"
    result = runner.invoke(
        wbstata, [f"{invalid_file}", "--target-version", "13", "--verbose"]
    )
    assert result.exit_code != 0
    assert (
        f"Error: {invalid_file} is not a valid path to a dta file."
        in result.output
    )

    # Check that error is caught one if the files does not exist
    result = runner.invoke(
        wbstata, [f"{dta1}", f"{invalid_file}", "--target-version", "13", "--verbose"]
    )
    assert result.exit_code == 0
    assert (
        f"Error: {invalid_file} is not a valid path to a dta file."
        in result.output
    )
    assert COMPLETION_MSG in result.output

    # Check that overwrite works
    # Warning should be present without verbose option
    OVERWRITE_WARNING = "Warning: you are writing over original input dta file."
    result = runner.invoke(
        wbstata, [f"{dta1}", "--target-version", "17", "--overwrite"]
    )
    assert result.exit_code == 0
    assert OVERWRITE_WARNING in result.output

    # Check that overwrite works with verbose
    _ver = 17
    result = runner.invoke(
        wbstata, [f"{dta1}", "--target-version", f"{_ver}", "--overwrite", "--verbose"]
    )
    assert result.exit_code == 0
    assert OVERWRITE_WARNING in result.output
    assert f"Done overwriting {dta1} in version {_ver}." in result.output

    # Check that overwrite works for multiple files work
    OVERWRITE_WARNING = "Warning: you are writing over original input dta file."
    result = runner.invoke(
        wbstata,
        [f"{dta1}", f"{dta2}" "--version", "17", "--overwrite", "--verbose"],
    )
    assert result.exit_code == 0
    assert OVERWRITE_WARNING in result.output
    assert COMPLETION_MSG in result.output

    # Check that using suffixes work
    result = runner.invoke(
        wbstata, [f"{dta1}", "--target-version", "13", "--suffix", "-suffix"]
    )
    assert result.exit_code == 0

    # Check that messages are correct if no valid dta files are found
    result = runner.invoke(wbstata, ["--all", "--target-version", "13", "--verbose"])
    assert result.exit_code == 0
    assert "dta files entered:" in result.output
    assert "Valid dta files to be converted:" in result.output
    assert "Nothing to convert." in result.output

    # Check that messages are correct with recursion
    result = runner.invoke(
        wbstata, ["--all", "--target-version", "13", "--verbose", "--recursive"]
    )
    assert result.exit_code == 0
    assert "dta files entered:" in result.output
    assert "Valid dta files to be converted:" in result.output
    assert "Conversions complete." in result.output
