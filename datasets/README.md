## Datasets

* All `dta` datasets in `./nickchk-causaldata/` are from Nick C. Huntington-Klein's [causaldata](https://github.com/NickCH-K/causaldata/tree/main/Stata) package.
* All other `dta` datasets are from the ones shipped in Stata 17. These `dta` files are listed in [`manifest.txt`](https://github.com/LSYS/wbStata/blob/main/datasets/manifest.txt).

## Scripts

* [`getdata.do`](https://github.com/LSYS/wbStata/blob/main/datasets/getdata.do) downloads the `dta` files listed in `manifest.txt` from Stata 17.
* [`txt2macro.ado`](https://github.com/LSYS/wbStata/blob/main/datasets/txt2macro.ado) is an `ado` utility that converts the `dta` files listed in `manifest.txt`into a Stata `macro`.
* [`opentest.do`](https://github.com/LSYS/wbStata/blob/main/datasets/testopen.do) tests and check that (a) the downloaded `dta` files from Stata 17 cannot be opened in Stata 13 and (b) the converted `dta` files (using `wbstata` and the default saving prefix `-wbstata`, e.g., with `auto-wbstata.dta`) can indeed be opened in Stata 13.
* [`opentest-log.txt`](https://github.com/LSYS/wbStata/blob/main/datasets/opentest-log.txt) logs the output from `opentest.do`.
