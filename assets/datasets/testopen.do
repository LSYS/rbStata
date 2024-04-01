local rootdir D:/wbStata/datasets // for my convenience to set project root dir, comment out to avoid conflict
cd `rootdir'
cap log close
log using testopen-log.txt, replace text
version 13

txt2macro manifest.txt
local datasets `r(mymacro)'
dis "`datasets'"

* Should fail to open in Stata 13
foreach data of local datasets {
	cap use `rootdir'/`data'.dta, clear
	assert _rc==610
}

log close
