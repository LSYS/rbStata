"""Main user-facing function."""
import re
import warnings
from glob import glob
from pathlib import Path
from typing import Optional, Sequence

import click
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
    >>> is_dta_file("./datasets/auto.dta")
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
    >>> convert_dta("datasets/auto.dta", "datasets/doctest-out.dta", 13)

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
    >>> add_suffix("filename.dta", "-wbstata")
    'filename-wbstata.dta'

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
    'input-wbstata.dta'

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
                filename = add_suffix(file, "-wbstata")
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


CONTEXT_SETTINGS = dict(
    help_option_names=("-h", "--help"),
    max_content_width=90,
)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument(
    "files", nargs=-1, required=False, type=str, metavar="<dta files>"
)
@click.option(
    "-t",
    "--target-version",
    help="Which version of Stata to convert to.",
    type=int,
    metavar="<int>",
)
@click.option(
    "-a",
    "--all",
    help="Convert all dta files in path.",
    is_flag=True,
    flag_value=True,
)
@click.option(
    "-s",
    "--suffix",
    help="Suffix to be added to converted file.",
    type=str,
    metavar="<text>",
)
@click.option(
    "-o",
    "--output",
    help="Name of converted .dta file (Single file conversion only). Supercedes [suffix].",
    type=str,
    default="[filename]-v[version].dta (e.g., auto-v13.dta)",
    metavar="<text>",
)
@click.option(
    "-r",
    "--recursive",
    help="Convert all .dta files in directory and subdirectories.",
    is_flag=True,
    flag_value=True,
)
@click.option(
    "-w",
    "--overwrite",
    help="Over[w]rite original input .dta files.",
    is_flag=True,
    flag_value=True,
)
@click.option(
    "-v", "--verbose", help="Print messages.", is_flag=True, flag_value=True
)
def wbstata(
    files: Sequence[str],
    target_version: Optional[int],
    suffix: Optional[str],
    output: Optional[str],
    all: bool = False,
    overwrite: bool = False,
    recursive: bool = False,
    verbose: bool = False,
) -> None:
    """Find your way back to older versions of dta files.

    Convert newer Stata .dta files to older versions so that you can open them
    in older Stata versions.

    Parameters
    ----------
    files: list-like
        List of dta files to be converted.
    target_version: int
        Stata version to convert to.
    suffix: str
        (Optional) Suffix string to be added to filename.
    output: str
        (Optional) Filename for output. If None, use suffix to create output name.
    all: bool
        If True, glob the dta files in path. Default is False.
    overwrite: bool
        If True, overwrite existing input (source) file. Default is False.
    recursive: bool
        If True, glob dta files in subdirectories. Default is False.
    verbose: bool
        If True, print messages to stdout. Default is False.

    Returns
    -------
    None
    """
    if (len(files) == 0) and (not all):
        PROMPT = True
        click.echo(
            "-------------------------------------------------------------\n"
            "Welcome to the wbStata quickstart command-line utility.\n\n"
            "You will be prompted for relevant settings.\n\n"
            "Please enter values under the following settings.\n"
            "(just press Enter to accept the default value in brackets)\n"
            "-------------------------------------------------------------\n"
        )
        # Prompt for dta file to convert
        click.echo(
            "Enter the dta file(s) you want to convert (e.g. ''auto.dta'').\n"
            "(It is not necessary to key in the .dta extension (e.g., just type ''auto'').\n"
            "Press Enter to include all .dta files in the current directory.)"
        )
        _files = click.prompt("> .dta file(s)", type=str, default="*")
    else:
        PROMPT = False

    # Prompt for target vresion
    if target_version is None:
        click.echo("\nThe Stata version to convert to.")
        target_version = click.prompt("> Target version", type=int, default=13)

    # Prompt for suffix to save with
    if PROMPT and (suffix is None) and (len(files) != 1):
        click.echo(
            "\nFile suffix for saving the output file(s).\n"
            "(For example, the suffix ''-old'' means that auto.dta will be converted and\n"
            "saved as auto-old.dta. Default is to use ''-wbstata''.)"
        )
        suffix = click.prompt(
            "> File suffix for saving",
            type=str,
            default="-wbstata",
        )
    if PROMPT and (len(files) == 1):
        filename_no_extension = files[0].split(".dta")[0]
        click.echo(
            "\nFile name for saving. Default is to save using the ''-wbstata'' suffix. For"
            "example, ''auto.dta'' will be converted and saved as auto-wbstata.dta."
        )
        output = click.prompt(
            "> Save file as",
            type=str,
            default=f"{filename_no_extension}-wbstata.dta",
        )
    else:
        output = None

    # Prompt for whether to glob dta files in subdirectories
    if PROMPT and (_files == "*"):
        click.echo(
            "\nInclude all .dta files in current directory and its subdirectories.\n"
            "(Default is to include only the .dta files in the current directory.)"
        )
        recursive = click.prompt(
            "> Include subdirectories (y/n)",
            type=click.BOOL,
            default="n",
        )

    # Consolidate files to convert
    if PROMPT:
        if _files == "*":
            files = glob_dta_files(recursive=recursive)
        else:
            files = _files.split(" ")
    elif all:
        files = glob_dta_files(recursive=recursive)

    # Prompt for whether to be verbose about messages
    if PROMPT:
        verbose = click.prompt(
            "\n> Print all messages (y/n)", type=click.BOOL, default="y"
        )
    if verbose:
        click.echo(f"+ dta files entered: {files}")

    files = [normalize_filename(f) for f in files]
    files = [normalize_dta_filename(f) for f in files]

    if verbose:
        click.echo(f"+ Valid dta files to be converted: {files}")

    OVERWRITE_WARNING = (
        "+ Warning: you are writing over original input dta file."
    )
    # Conversion for a single file
    if len(files) == 1:
        filename = files[0]
        assert is_dta_file(filename)
        if overwrite:
            click.echo(OVERWRITE_WARNING)
            convert_dta(filename, filename, target_version)
            if verbose:
                click.secho("+ Converted: ", fg="green", bold=True, nl=False)
                click.echo(
                    f"Done overwriting {filename} in version {target_version}."
                )
        else:
            out = get_output_name(
                filename,
                overwrite=overwrite,
                output=output,
                suffix=suffix,
            )
            convert_dta(filename, out, target_version)
            if verbose:
                click.secho("+ Converted: ", fg="green", bold=True, nl=False)
                click.echo(f"{filename} to {out} in version {target_version}.")
    # Conversion for batch of files
    else:
        with click.progressbar(
            files, label="Converting", length=len(files)
        ) as pb_files:
            for file in pb_files:
                try:
                    is_dta_file(file)
                except ClickException:
                    click.secho(
                        f"Error: {file} is not a valid path to a dta file.",
                        fg="red",
                        err=True,
                    )
                    continue
                if overwrite:
                    click.echo(OVERWRITE_WARNING)
                    convert_dta(file, file, target_version)
                    if verbose:
                        click.secho(
                            "+ Converted: ", fg="green", bold=True, nl=False
                        )
                        click.echo(
                            f"Done overwriting {file} in version {target_version}."
                        )
                else:
                    out = get_output_name(
                        file,
                        overwrite=overwrite,
                        output=output,
                        suffix=suffix,
                    )
                    convert_dta(file, out, target_version)
                    # if False:
                    #     click.secho(
                    #         "+ Converted: ", fg="green", bold=True, nl=False
                    #     )
                    #     click.echo(f"{file} to {out} in version {target_version}.")

    if verbose:
        if len(files) > 0:
            click.secho("Success: ", fg="green", bold=True, nl=False)
            click.echo("Conversions complete.")
        else:
            click.echo("+ Nothing to convert.")
