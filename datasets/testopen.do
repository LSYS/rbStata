local rootdir D:/wbStata/datasets // for my convenience to set project root dir, comment out to avoid conflict
cd `rootdir'
cap log close
log using opentest-log.txt, replace text
version 13

txt2macro manifest.txt
local datasets `r(mymacro)'
dis "`datasets'"

* Should fail to open in Stata 13
foreach data of local datasets {
	cap use `rootdir'/`data'.dta
	assert _rc==610
}

* Should open in Stata 13
foreach data of local datasets {
	cap use `rootdir'/wbstata/`data'-wbstata.dta
	assert _rc==0
}

log close
