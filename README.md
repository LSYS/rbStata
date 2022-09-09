# wbStata

Find your way back to older versions of Stata `.dta` files.


## Statement of Need

Stata `.dta` data files are not forward compatible. 
This means you cannot use older versions (e.g., `Stata 13`) to read a `.dta` file exported from newer versions (e.g., `Stata 17`).

So what is one to do when you try to open a `dta` file in Stata and get a rude `dta too modern r(601)` error:
<details open><summary></summary>
  <p align="center"><img width="100%" src="./assets/gfy-error.png"></p>
</details>

`wbStata` is a quick and simple CLI (command-line interface) to go way back with Stata data (`.dta`) files.


## Quick usage

Show help documentation: `wbstata -h`
```console
$ wbstata -h
Usage: wbstata [OPTIONS] <dta files>

  Find your way back to older versions of dta files.

  Convert newer Stata .dta files to older versions so that you can open them in older
  Stata versions.

Options:
  -v, --version <int>  Which version of Stata to convert to.
  -s, --suffix <text>  Suffix to be added to converted file.
  -o, --output <text>  Name of converted .dta file (Single file conversion only).
                       Supercedes [suffix].
  -w, --overwrite      Over[w]rite original input .dta files.
  -ve, --verbose       Print messages.
  -h, --help           Show this message and exit.
```

## Alternative tools

## More about the problem
* [[1]](https://www.stata.com/support/faqs/data-management/save-for-previous-version/) Stata support FAQs: How can I save a Stata dataset so that it can be read by a previous version of Stata?
* [[2]](https://www3.nd.edu/~rwilliam/stats/stataconversions.html) Stata data files: Reading and writing to and from different file formats


## About this utility
`wbStata` is a CLI utility to easily convert between (or, go way back to) versions of Stata's `.dta`, which are not forward compatible. 

This utility wraps around [`click`](https://click.palletsprojects.com/) and [`pandas`](https://github.com/pandas-dev/pandas)'s [`DataFrame.to_Stata`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_stata.html) utility.
