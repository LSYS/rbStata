from wbStata.cli import normalize_dta_filename
from wbStata.cli import convert_dta
from wbStata.cli import add_suffix
from wbStata.cli import get_output_name


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
