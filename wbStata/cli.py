import click
from click import ClickException
from typing import Sequence, Optional
from pathlib import Path
import re
import pandas as pd
from glob import glob


def normalize_filename(filename: str) -> str:
    """Normalize filenames by removing whitespaces and lower casing."""
    # Remove extra whitespaces
    re_extra_whitespaces = re.compile(r"\s+")
    filename = re_extra_whitespaces.sub("", filename).strip()
    filename = filename.lower()
    return filename


def normalize_dta_filename(filename: str) -> str:
    """Ensure that string for filename to write to is normalize with .dta extension."""
    dta_filename = Path(filename)
    if dta_filename.suffix != ".dta":
        filename = "".join([filename, ".dta"])
        return filename
    else:
        return filename


def is_dta_file(filename: str) -> bool:
    """Check if filename is a valid path to a dta file."""
    path = Path(filename)
    if path.suffix == ".dta":
        is_dta = True
    else:
        is_dta = False

    if (path.is_file()) and (is_dta):
        return True
    else:
        raise ClickException(f"{filename} is not a valid path to a dta file.")


def convert_dta(input: str, output: str, version) -> None:
    """Convert dta file."""
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
    version = map_versions[version]
    pd.read_stata(input).to_stata(output, version=version, write_index=False)


def add_suffix(filename: str, suffix: str) -> str:
    """Add suffix to filename."""
    filename, ext = filename.split(".")
    filename = "".join([filename, suffix, ".", ext])
    return filename


def get_output_name(
    file: str,
    version: int,
    overwrite: bool,
    suffix: Optional[str] = None,
    output: Optional[str] = None,
) -> str:
    """Get output name for the file to be saved."""
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
                filename = add_suffix(file, f"-v{version}")
                return filename


CONTEXT_SETTINGS = {
    "help_option_names": ("-h", "--help"),
    "max_content_width": 90,
}


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument(
    "files", nargs=-1, required=False, type=str, metavar="<dta files>"
)
@click.option(
    "-v",
    "--version",
    help="Which version of Stata to convert to.",
    type=int,
    metavar="<int>",
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
    "-ve", "--verbose", help="Print messages.", is_flag=True, flag_value=True
)
def wbstata(
    files: Sequence[str],
    version: Optional[int],
    suffix: Optional[str],
    output: Optional[str],
    recursive: bool,
    overwrite: bool,
    verbose: bool,
) -> None:
    """Find your way back to older versions of dta files.

    Convert newer Stata .dta files to older versions so that you can open them
    in older Stata versions.
    """
    if len(files) == 0:
        PROMPT = True
        _files = click.prompt(".dta file(s)", type=str, default="*")
    else:
        PROMPT = False

    if PROMPT and (_files == "*"):
        recursive = click.prompt(
            "Include .dta files in subdirectories (y/n)",
            type=click.BOOL,
            default="n",
        )

    if PROMPT:
        if _files == "*":
            if recursive:
                files = glob("**/*.dta", recursive=recursive)
            else:
                files = glob("*.dta")
        else:
            files = _files.split(" ")

    if version is None:
        version = click.prompt(
            "Which version to convert to?", type=int, default=13
        )

    if PROMPT and (suffix is None):
        suffix = click.prompt(
            "Convert and save file using suffix",
            type=str,
            default=f"-v{version}",
        )
    if PROMPT and (len(files) == 1):
        filename_no_extension = files[0].split(".dta")[0]
        output = click.prompt(
            "Convert and save file as",
            type=str,
            default=f"{filename_no_extension}-v{version}.dta",
        )
    else:
        output = None
    # click.echo(files)
    # import sys
    # if files==["*"]:
    #     files = [file for file in files if ".dta" in file]
    # click.echo(files)
    # sys.exit(1)

    files = [normalize_filename(f) for f in files]
    files = [normalize_dta_filename(f) for f in files]

    OVERWRITE_WARNING = "Warning: you are writing over original input dta file."
    if len(files) == 1:
        filename = files[0]
        assert is_dta_file(filename)
        if overwrite:
            click.echo(OVERWRITE_WARNING)
            convert_dta(filename, filename, version)
            if verbose:
                click.echo(f"Done overwriting {filename} in version {version}.")
        else:
            out = get_output_name(
                filename,
                version=version,
                overwrite=overwrite,
                output=output,
                suffix=suffix,
            )
            convert_dta(filename, out, version)
            if verbose:
                click.echo(
                    f"Done writing {filename} to {out} in version {version}."
                )
    else:
        for file in files:
            try:
                is_dta_file(file)
            except ClickException:
                click.echo(
                    f"Error: {file} is not a valid path to a dta file.",
                    err=True,
                )
                continue
            if overwrite:
                click.echo(OVERWRITE_WARNING)
                convert_dta(file, file, version)
                if verbose:
                    click.echo(f"Done overwriting {file} in version {version}.")
            else:
                out = get_output_name(
                    file,
                    version=version,
                    overwrite=overwrite,
                    output=output,
                    suffix=suffix,
                )
                convert_dta(file, out, version)
                if verbose:
                    click.echo(
                        f"Done writing {file} to {out} in version {version}."
                    )

    if verbose:
        click.echo("Conversions complete.")
