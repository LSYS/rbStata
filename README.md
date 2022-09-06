# wbStata

A quick and dirty CLI (command-line interface) to go way back with Stata data (`.dta`) files.

### Statement of Need

Stata `.dta` data files are not forward compatible. 
This means you cannot use older versions (e.g., Stata 13) to read a `.dta` file exported from newer versions (e.g., Stata 17).

So what is one to do when colleagues or classmates send you a `.dta` from their newer version of Stata and you end up with the following error because you have no access to newer Stata versions?

### Quick usage


### Alternative tools

### More about the problem
* [[1]](https://www.stata.com/support/faqs/data-management/save-for-previous-version/) Stata support FAQs: How can I save a Stata dataset so that it can be read by a previous version of Stata?
* [[2]](https://www3.nd.edu/~rwilliam/stats/stataconversions.html) Stata data files: Reading and writing to and from different file formats


### About this utility
`wbStata` is a CLI utility to easily convert between (or, go way back to) versions of Stata's `.dta`, which are not forward compatible. 

This utility wraps around [`click`](https://click.palletsprojects.com/) and [`pandas`](https://github.com/pandas-dev/pandas)'s [`DataFrame.to_Stata`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_stata.html) utility.
