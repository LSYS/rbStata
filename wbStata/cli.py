import click
from typing import Sequence, Optional
from pathlib import Path
import re


def normalize_filename(filename):
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


import pandas as pd


def convert_dta(input, output, version=13):
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
    pd.read_stata(input).to_stata(output, version=version)


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
    # 'token_normalize_func': lambda filename: normalize_filename(filename)
}

# File = click.File(mode="r", encoding=None, errors="strict", lazy=True)
File = str


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("files", nargs=-1, required=False, type=File, metavar="<dta files>")
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
    "-w",
    "--overwrite",
    help="Over[w]rite original input .dta files.",
    is_flag=True,
    flag_value=True,
)
@click.option("-ve", "--verbose", help="Print messages.", is_flag=True, flag_value=True)
def wbstata(
    files: Sequence[str],
    version: Optional[int],
    suffix: Optional[str],
    # prefix: Optional[str],
    output: Optional[str],
    overwrite: bool,
    verbose: bool,
) -> None:
    """Find your way back to older versions of dta files.

    Convert newer Stata .dta files to older versions so that you can open them
    in older Stata versions.
    """
    if len(files) == 0:
        PROMPT = True
        _files = click.prompt("Which .dta file(s) to convert", type=File, default="*")
        files = _files.split(" ")
    else:
        PROMPT = False

    if version is None:
        version = click.prompt("Which version to convert to?", type=int, default=13)

    if PROMPT and (suffix is None):
        suffix = click.prompt(
            "Convert and save file using suffix", type=str, default=""
        )
    if PROMPT and (len(files) == 1):
        output = click.prompt(
            "Convert and save file as", type=str, default=f"{files[0]}-v{version}.dta"
        )
    else:
        output = None

    files = [normalize_filename(f) for f in files]
    files = [normalize_dta_filename(f) for f in files]

    if len(files) == 1:
        filename = files[0]
        if overwrite:
            convert_dta(filename, filename, version)
        else:
            out = get_output_name(
                filename,
                version=version,
                overwrite=overwrite,
                output=output,
                suffix=suffix,
            )
            convert_dta(filename, out, version)
    else:
        for file in files:
            if overwrite:
                convert_dta(file, file, version)
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
            f"Converting {files} to Stata version {version} and saving to {output}"
        )
