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


def convert_dta(input: str, output: str, target_version) -> None:
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
    version = map_versions[target_version]
    pd.read_stata(input).to_stata(output, version=version, write_index=False)


def add_suffix(filename: str, suffix: str) -> str:
    """Add suffix to filename."""
    filename, ext = filename.split(".")
    filename = "".join([filename, suffix, ".", ext])
    return filename


def get_output_name(
    file: str,
    target_version: int,
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
                filename = add_suffix(file, f"-v{target_version}")
                return filename


def glob_dta_files(recursive: bool) -> list:
    """Get all files with .dta extension"""
    if recursive:
        files = glob("**/*.dta", recursive=recursive)
    else:
        files = glob("*.dta", recursive=recursive)
    return files


CONTEXT_SETTINGS = {
    "help_option_names": ("-h", "--help"),
    "max_content_width": 90,
}


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
    """
    if (len(files) == 0) and (not all):
        PROMPT = True
        click.echo(
            "-------------------------------------------------------------"
        )
        click.echo("Welcome to the wbStata quickstart command-line utility.\n")
        click.echo("You will be prompted for relevant settings.\n")
        click.echo("Please enter values under the following settings.")
        click.echo("(just press Enter to accept the default value in brackets)")
        click.echo(
            "-------------------------------------------------------------\n"
        )
        click.echo(
            "Enter the dta file(s) you want to convert (e.g. ''auto.dta''). It is not"
        )
        click.echo(
            "necessary to key in the .dta extension (e.g. just type ''auto''). Press"
        )
        click.echo("Enter to include all .dta files in the current directory.")
        _files = click.prompt("> .dta file(s)", type=str, default="*")
    else:
        PROMPT = False

    if PROMPT and (_files == "*"):
        click.echo(
            "\nInclude all .dta files in current directory and its subdirectories. Default"
        )
        click.echo(
            "is to include only the .dta files in the current directory."
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

    # Prompt outstanding settings
    if target_version is None:
        click.echo(
            "\nThe Stata version do you want to convert to. This is equivalently the"
        )
        click.echo("version of Stata you have.")
        target_version = click.prompt("> Target version", type=int, default=13)

    if PROMPT and (suffix is None) and (len(files) != 1):
        click.echo(
            "\nFile suffix for saving the output file(s). For example, the suffix ''-old''"
        )
        click.echo(
            "means that auto.dta will be converted and saved as auto-old.dta. Default"
        )
        click.echo(f"is to use ''-v{target_version}''.")
        suffix = click.prompt(
            "> File suffix for saving",
            type=str,
            default=f"-v{target_version}",
        )
    if PROMPT and (len(files) == 1):
        filename_no_extension = files[0].split(".dta")[0]
        click.echo(
            f"\nFile name for saving. Default is to save using the ''-v{target_version}'' suffix. For"
        )
        click.echo(
            f"example, ''auto.dta'' will be converted and saved as auto-v{target_version}.dta."
        )
        output = click.prompt(
            "> Save file as",
            type=str,
            default=f"{filename_no_extension}-v{target_version}.dta",
        )
    else:
        output = None

    if PROMPT:
        click.echo("\nPrint all messages.")
        verbose = click.prompt(
            "> Print messages (y/n)", type=click.BOOL, default="y"
        )

    click.echo("")
    if verbose:
        click.echo(f"+ dta files entered: {files}")

    files = [normalize_filename(f) for f in files]
    files = [normalize_dta_filename(f) for f in files]

    if verbose:
        click.echo(f"+ Valid dta files to be converted: {files}")

    OVERWRITE_WARNING = (
        "+ Warning: you are writing over original input dta file."
    )
    if len(files) == 1:
        filename = files[0]
        assert is_dta_file(filename)
        if overwrite:
            click.echo(OVERWRITE_WARNING)
            convert_dta(filename, filename, target_version)
            if verbose:
                click.secho("+ Converted: ", fg="green", bold=True, nl=False)
                click.echo(f"Done overwriting {filename} in version {target_version}.")
        else:
            out = get_output_name(
                filename,
                target_version=target_version,
                overwrite=overwrite,
                output=output,
                suffix=suffix,
            )
            convert_dta(filename, out, target_version)
            if verbose:
                click.secho("+ Converted: ", fg="green", bold=True, nl=False)
                click.echo(f"{filename} to {out} in version {target_version}.")
    else:
        for file in files:
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
                    click.echo(f"Done overwriting {file} in version {target_version}.")
            else:
                out = get_output_name(
                    file,
                    target_version=target_version,
                    overwrite=overwrite,
                    output=output,
                    suffix=suffix,
                )
                convert_dta(file, out, target_version)
                if verbose:
                    click.secho(
                        "+ Converted: ", fg="green", bold=True, nl=False
                    )
                    click.echo(f"{file} to {out} in version {target_version}.")

    if verbose:
        if len(files) > 0:
            click.secho("Success: ", fg="green", bold=True, nl=False)
            click.echo("Conversions complete.")
            from termcolor import colored
        else:
            click.echo("+ Nothing to convert.")
