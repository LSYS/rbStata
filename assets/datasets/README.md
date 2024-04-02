## Datasets

* All `dta` datasets in `./nickchk-causaldata/` are from Nick C. Huntington-Klein's [causaldata](https://github.com/NickCH-K/causaldata/tree/main/Stata) package.
* All other `dta` datasets are from the ones shipped in Stata 17. These `dta` files are listed in [`manifest.txt`](https://github.com/LSYS/wbStata/blob/main/datasets/manifest.txt).

## Scripts

* [`txt2macro.ado`](https://github.com/LSYS/wbStata/blob/main/datasets/txt2macro.ado) is an `ado` utility that converts the `dta` files listed in `manifest.txt`into a Stata `macro`.
* [`getdata.do`](https://github.com/LSYS/wbStata/blob/main/datasets/getdata.do) downloads the `dta` files listed in `manifest.txt` from Stata 17.
* [`testopen.do`](https://github.com/LSYS/wbStata/blob/main/datasets/testopen.do) tests and check that the downloaded `dta` files from Stata 17 cannot be opened in Stata 13.
* [`opentest-log.txt`](https://github.com/LSYS/wbStata/blob/main/datasets/opentest-log.txt) logs the output from `opentest.do`.
* [`testopen-converted.do`](https://github.com/LSYS/wbStata/blob/main/datasets/testopen-converted.do) tests and check that and the converted `dta` files (using the default saving prefix `-wbstata`, e.g., with `auto-wbstata.dta`) can indeed be opened in Stata 13.
* [`opentest-converted-log.txt`](https://github.com/LSYS/wbStata/blob/main/datasets/opentest-log.txt) logs the output from `opentest-converted.do`.

## Make
* To download the `dta` files shipped with Stata 17, type
  ```Makefile
  make getdata
  ```
  from a machine with access to Stata 17.
  
* To test all conversion works, type
  ```Makefile
  make test
  ```
  in a mchine with access to an older Stata version (e.g., Stata 13) and where `wbstata` is installed. Test that conversion works will require the `wbstata` installation.