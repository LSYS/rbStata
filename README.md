# wbStata

`wbStata` is a CLI utility to easily convert between (or, go way back to) versions of Stata's `.dta`, which are not forward compatible. 



## Statement of Need

Stata `.dta` data files are not forward compatible. 
This means you cannot use older versions (e.g., `Stata 13`) to read a `.dta` file exported from newer versions (e.g., `Stata 17`).

So what is one to do when you try to open a `dta` file in Stata and get a rude `dta too modern r(601)` error:
<details open><summary>...</summary>
  <p align="center"><img width="100%" src="./assets/gfy-error.png"></p>
</details>

Find your way back to older versions of Stata `.dta` files with `wbStata`.
`wbStata` is a quick and dead simple CLI (command-line interface) to go way back with Stata data (`.dta`) files. You *do not need access to* newer `Stata` versions.


## Quick usage

* **Simple and Single-line command-line usage:**
  * Convert the `auto.dta` file so that you can open it in Stata 13
    <pre>$ wbstata auto.dta --version 13 --verbose</pre>
  
  
  * Convert all `dta` files in the path so that you can open it in Stata 13
    <pre>$ wbstata --all --version 13 --verbose</pre>
  
  
  
  

* **Let `wbStata` prompt you for relevant settings:** <br>
  (press enter to accept default settings in brackets)
  * `dta file(s)` [*]: `dta file(s)` to be converted 
  * `version` [13]: `version` to convert to (or the `Stata` version you have)





## Alternative tools

## More about the problem
* [[1]](https://www.stata.com/support/faqs/data-management/save-for-previous-version/) Stata support FAQs: How can I save a Stata dataset so that it can be read by a previous version of Stata?
* [[2]](https://www3.nd.edu/~rwilliam/stats/stataconversions.html) Stata data files: Reading and writing to and from different file formats


## About this utility
`WbStata` wraps around [`click`](https://click.palletsprojects.com/) and [`pandas`](https://github.com/pandas-dev/pandas)'s [`DataFrame.to_Stata`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_stata.html) utility. Using `wbStata`, easily convert new Stata `dta` files to older versions.

<details><summary>Show CLI help reference</summary>
  
  ```console
  $ wbstata -h
  Usage: wbstata [OPTIONS] <dta files>

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
  

