"""Helpers."""
import re
import warnings
from glob import glob
from pathlib import Path
from typing import Optional

import pandas as pd
from anyascii import anyascii
from click import ClickException

warnings.simplefilter(action="ignore", category=Warning)


def normalize_filename(filename: str) -> str:
    """Normalize filenames by removing whitespaces.

    Parameters
    ----------
    filename: str

    Examples
    --------
    >>> normalize_filename("File.dta")
    'File.dta'
    >>> normalize_filename("     File.dta     ")
    'File.dta'

    Returns
    -------
    Str
    """
    # Remove extra whitespaces
    re_extra_whitespaces = re.compile(r"\s+")
    filename = re_extra_whitespaces.sub("", filename).strip()
    return filename


def normalize_dta_filename(filename: str) -> str:
    """Ensure that string for filename to write to is normalized with .dta extension.

    Parameters
    ----------
    filename: str

    Examples
    --------
    >>> normalize_dta_filename("output")
    'output.dta'

    Returns
    -------
    Str
    """
    dta_filename = Path(filename)
    if dta_filename.suffix != ".dta":
        filename = "".join([filename, ".dta"])
        return filename
    else:
        return filename


def is_dta_file(filename: str) -> bool:
    """Check if filename is a valid path to a dta file.

    Parameters
    ----------
    filename: str

    Examples
    --------
    >>> is_dta_file("./assets/datasets/auto.dta")
    True

    Returns
    -------
    Bool

    Raises
    ------
    ClickException
        If the filename input does not point to a valid dta file.
    """
    path = Path(filename)
    if path.suffix == ".dta":
        is_dta = True
    else:
        is_dta = False

    if (path.is_file()) and (is_dta):
        return True
    else:
        raise ClickException(f"{filename} is not a valid path to a dta file.")


def convert_dta(input: str, output: str, target_version: int) -> None:
    """Convert dta file.

    This function takes care of mapping Stata versions to the versions
    recognized by pandas. The function also takes care of UnicodeEncodeError's
    by converting unicode strings to ascii using the anyascii package.

    Parameters
    ----------
    input: str
        Input (source) dta file to convert.
    output: str
        Output (destination) dta file after conversion.
    target_version: int
        Stata version to convert to.

    Example
    -------
    >>> convert_dta("assets/datasets/auto.dta", "assets/datasets/doctest-out.dta", 13)

    Returns
    -------
    None
    """
    map_versions = {
        10: 114,
        11: 114,
        12: 114,
        13: 117,
        14: 118,
        15: None,
        16: None,
        17: None,
    }
    version = map_versions[target_version]

    reader_obj = pd.read_stata(input, iterator=True)
    data_label = reader_obj.data_label
    variable_labels = reader_obj.variable_labels()

    # Variable labels must be 80 chars or fewer
    for key, val in variable_labels.items():
        if len(val) >= 80:
            variable_labels[key] = val[:80]

    std_opts_tostata = dict(
        version=version,
        write_index=False,
        data_label=data_label,
        variable_labels=variable_labels,
    )

    try:
        pd.read_stata(input).to_stata(output, **std_opts_tostata)
    except UnicodeEncodeError:
        df = pd.read_stata(input)
        for col in df.columns:
            try:
                df[col] = df[col].apply(lambda x: anyascii(x))
            except TypeError:
                pass
        df.to_stata(output, **std_opts_tostata)


def add_suffix(filename: str, suffix: str) -> str:
    """Add suffix to filename.

    Parameters
    ----------
    filename: str
        Filename that suffix is to be added to.
    suffix: str
        Suffix string to be added to filename.

    Examples
    --------
    >>> add_suffix("filename.dta", "-rbstata")
    'filename-rbstata.dta'

    >>> add_suffix("filename.dta", "")
    'filename.dta'

    Returns
    -------
    Str
        Filename with added suffix.
    """
    filename, ext = filename.split(".")
    filename = "".join([filename, suffix, ".", ext])
    return filename


def get_output_name(
    file: str,
    overwrite: bool,
    suffix: Optional[str] = None,
    output: Optional[str] = None,
) -> str:
    """Get output name for the file to be saved.

    Parameters
    ----------
    file: str
        Filename of file.
    overwrite: bool
        If True, overwrite existing input (source) file.
    suffix: str
        (Optional) Suffix string to be added to filename.
    output: str
        (Optional) Filename for output. If None, use suffix to create output name.

    Examples
    --------
    >>> get_output_name("input.dta", True)
    'input.dta'
    >>> get_output_name("input.dta", True, "-suffix")
    'input.dta'
    >>> get_output_name("input.dta", False, "-suffix")
    'input-suffix.dta'
    >>> get_output_name("input.dta", False, output="output.dta")
    'output.dta'
    >>> get_output_name("input.dta", False, output=None)
    'input-rbstata.dta'

    Returns
    -------
    Str
        Filename for saving the output.
    """
    if overwrite:
        return file
    else:
        if output is not None:
            return output
        else:
            if suffix is not None:
                filename = add_suffix(file, suffix)
                return filename
            else:
                filename = add_suffix(file, "-rbstata")
                return filename


def glob_dta_files(recursive: bool) -> list:
    """Get all files with .dta extension.

    Parameters
    ----------
    recursive: bool
        If True, include dta files in subdirectories.

    Returns
    -------
    List
        List of dta files to be batch converted.
    """
    if recursive:
        files = glob("**/*.dta", recursive=recursive)
    else:
        files = glob("*.dta", recursive=recursive)
    return files
