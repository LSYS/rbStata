# rbStata

`rbStata` is a CLI utility to easily convert between (or, roll back) versions of Stata's `.dta`, which are not forward compatible. 
* Cross-platform CLI utility: Windows, Mac, Linux.
* No knowledge of Python required (but requires a Python installation).
* Handles Unicode to ASCII transliteration (older versions of Stata do not support Unicode).
* Works with Python 3.6+.
* Handles transferring (where available and possible) of:
  - Variable labels
  - Data labels
  - Value labels

| | |
| --- | --- |
| Package | [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/rbStata?label=Python%203.6%2B&logo=python&logoColor=white)](https://pypi.org/project/rbStata/) [![PyPI](https://img.shields.io/pypi/v/rbStata?color=blue&label=PyPI&logo=pypi&logoColor=white)](https://pypi.org/project/rbStata/) [![GitHub release (latest by date)](https://img.shields.io/github/v/release/lsys/rbStata?color=blue&label=Latest%20release)](https://github.com/LSYS/rbStata/releases) |
| Testing/build | [![Coverage](https://codecov.io/github/lsys/rbStata/coverage.svg?branch=main)](https://codecov.io/gh/lsys/rbStata) [![CI](https://github.com/LSYS/rbStata/actions/workflows/build.yml/badge.svg)](https://github.com/LSYS/rbStata/actions/workflows/build.yml) [![CLI](https://github.com/LSYS/rbStata/actions/workflows/cli-pkg.yml/badge.svg)](https://github.com/LSYS/rbStata/actions/workflows/cli-pkg.yml) [![Pkg-CLI](https://github.com/LSYS/rbStata/actions/workflows/Pkg-CLI.yml/badge.svg)](https://github.com/LSYS/rbStata/actions/workflows/Pkg-CLI.yml) [![DocLinks](https://github.com/LSYS/rbStata/actions/workflows/doclinks.yml/badge.svg)](https://github.com/LSYS/rbStata/actions/workflows/doclinks.yml) |
| Meta | [![DOI](https://zenodo.org/badge/532792769.svg)](https://zenodo.org/doi/10.5281/zenodo.10925080) [![GitHub](https://img.shields.io/github/license/lsys/rbStata?color=purple&label=License)](https://choosealicense.com/licenses/mit/) |

## Statement of Need

Stata `.dta` data files are not forward compatible. 
This means you cannot use older versions (e.g., `Stata 13`) to read a `.dta` file exported from newer versions (e.g., `Stata 17`).

So what is one to do when you try to open a `dta` file in Stata and get a rude `dta too modern r(601)` error:
<details open><summary><em>...</em></summary>
  <p align="center"><img width="100%" src="https://raw.githubusercontent.com/LSYS/rbStata/main/assets/gfy-error.png"></p>
</details>

Roll back to older versions of Stata `.dta` files with `rbStata`.
`rbStata` is a quick and dead simple CLI (command-line interface) to go way back with Stata data (`.dta`) files. You *do not need access to* newer `Stata` versions.


## Quick usage

* **Simple single-line command-line usage:**
  * Convert the `auto.dta` file so that you can open it in Stata 13
    <pre>$ rbstata auto.dta --target-version 13 --verbose</pre>
  
  * Convert all `dta` files in the path so that you can open it in Stata 13
    <pre>$ rbstata --all --target-version 13 --verbose</pre>
  

* **Let `rbStata` prompt you for relevant settings:** <br>
  
  Type `rbstata` and enter settings (press enter to accept default settings in brackets):
  <pre>$ rbstata</pre>
  ```console
  -------------------------------------------------------------
  Welcome to the rbStata quickstart command-line utility.

  You will be prompted for relevant settings.

  Please enter values under the following settings.
  (just press Enter to accept the default value in brackets)
  -------------------------------------------------------------

  Enter the dta file(s) you want to convert (e.g. ''auto.dta'').
  (It is not necessary to key in the .dta extension (e.g., just type ''auto'').
  Press Enter to include all .dta files in the current directory.)
  > .dta file(s) [*]:
  ...

  The Stata version to convert to.
  > Target version [13]:
  ...
  
  File suffix for saving the output file(s).
  (For example, the suffix ''-old'' means that auto.dta will be converted and
  saved as auto-old.dta. Default is to use ''-rbstata''.)
  > File suffix for saving [-rbstata]:
  ...
  
  Include all .dta files in current directory and its subdirectories.
  (Default is to include only the .dta files in the current directory.)
  > Include subdirectories (y/n) [n]:
  ...
  
  > Print all messages (y/n) [y]:
  ...
  ```
<details><summary><em>Settings [defaults]</em></summary>

  * `.dta file(s)` [*]: .dta files to convert [all .dta files in current directory]
  * `Target version [13]`: version to convert to [Stata v13]  
  * `File suffix for saving [-rbstata]`: Suffix for saving [E.g. save auto.dta to auto-rbstata.dta]
  * `Include subdirectories (y/n) [n]`: Include subdirectories if * [no]
  * `Print all messages (y/n) [y]`: Print all messages and errors [yes]
</details>

## More about the problem
<details open><summary><em>Assortment of enquires about the error</em></summary>
  
  * [[1]](https://www.stata.com/support/faqs/data-management/save-for-previous-version/) Stata support FAQs: How can I save a Stata dataset so that it can be read by a previous version of Stata?
  * [[2]](https://www.statalist.org/forums/forum/general-stata-discussion/general/1440296-how-to-read-a-stata-15-data-file-in-stata-13) how to read a stata 15 data file in stata 13.
  * [[3]](https://www.statalist.org/forums/forum/general-stata-discussion/general/1326849-how-to-open-stata-14-files-in-stata-12-13) How to open stata 14 files in Stata 12-13.
  * [[4]](https://www.statalist.org/forums/forum/general-stata-discussion/general/1373797-how-to-open-a-new-stata-dataset-version) How to open a new stata dataset version.
  * [[5]](https://www.statalist.org/forums/forum/general-stata-discussion/general/1363089-how-to-open-a-file-that-is-more-from-a-more-recent-version-of-stata-into-stata13) How to open a file that is more from a more recent version of Stata into Stata13.
  <!-- Deadlink -->
  <!-- * [[6]](https://www.reddit.com/r/stata/comments/4ufos2/convert_stata_14_dta_file_t) Convert Stata 14 .dta file to Stata 13. -->
</details>  

## Versions and string handling

One major jump in forward compatibility is from Stata 13 to Stata 14, where Stata 14 started adding Unicode compatibility. `rbStata` handles transferring of the data, value, and variable labels. If Unicode in labels exist and the backward target version is 13, `rbStata` will transliterate Unicode to ASCII *and* truncate labels to 80 characters.

<details open><summary><em>Assortment of enquires about the error</em></summary>
  
  * [[1]](https://www.stata.com/support/faqs/data-management/save-for-previous-version/) Stata support FAQs: How can I save a Stata dataset so that it can be read by a previous version of Stata?
  * [[2]](https://www.statalist.org/forums/forum/general-stata-discussion/general/1440296-how-to-read-a-stata-15-data-file-in-stata-13) how to read a stata 15 data file in stata 13.
  * [[3]](https://www.statalist.org/forums/forum/general-stata-discussion/general/1326849-how-to-open-stata-14-files-in-stata-12-13) How to open stata 14 files in Stata 12-13.
  * [[4]](https://www.statalist.org/forums/forum/general-stata-discussion/general/1373797-how-to-open-a-new-stata-dataset-version) How to open a new stata dataset version.
  * [[5]](https://www.statalist.org/forums/forum/general-stata-discussion/general/1363089-how-to-open-a-file-that-is-more-from-a-more-recent-version-of-stata-into-stata13) How to open a file that is more from a more recent version of Stata into Stata13.
  <!-- Deadlink -->
  <!-- * [[6]](https://www.reddit.com/r/stata/comments/4ufos2/convert_stata_14_dta_file_t) Convert Stata 14 .dta file to Stata 13. -->
</details>  

## Alternative solutions
Based on proposed solutions in [More about the problem](#more-about-the-problem).
* [[0]](https://www.stata.com/manuals/dsave.pdf) Use Stata's `saveold` (but for this you first need access to the new Stata version. Read in the `dta` file. Save it using `saveold`. Then use the converted `dta` file in your older Stata version).
* [[1]](https://stattransfer.com/) Stat/Transfer (proprietary).
* [[2]](https://cran.r-project.org/web/packages/haven/index.html) R's `Haven`.

## About this utility
`rbStata` is an open source utility that wraps around [`click`](https://click.palletsprojects.com/) and [`pandas`](https://github.com/pandas-dev/pandas)'s [`DataFrame.to_Stata`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_stata.html) utility. Using `rbStata`, easily convert new Stata `dta` files to older versions.

<details><summary><em>Expose CLI help reference</em></summary>
  
  ```console
  $ rbstata -h
  Usage: rbstata [OPTIONS] <dta files>

    Find your way back to older versions of dta files.

    Convert newer Stata .dta files to older versions so that you can open them in older
    Stata versions.

  Options:
    -a, --all            Convert all dta files in path.
    -v, --version <int>  Which version of Stata to convert to.
    -s, --suffix <text>  Suffix to be added to converted file.
    -o, --output <text>  Name of converted .dta file (Single file conversion only).
                         Supercedes [suffix].
    -r, --recursive      Convert all .dta files in directory and subdirectories.
    -w, --overwrite      Over[w]rite original input .dta files.
    -ve, --verbose       Print messages.
    -h, --help           Show this message and exit.
  ```
</details>
  

