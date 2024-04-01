local rootdir D:/wbStata/datasets/ // for my convenience to set project root dir, comment out to avoid conflict
cd `rootdir'
cap log close
log using testopen-converted-log.txt, replace text
version 13

txt2macro manifest.txt
local datasets `r(mymacro)'
dis "`datasets'"

foreach data of local datasets {
	local converted_datasets `converted_datasets' `data'-wbstata
}
dis "`converted_datasets'"

* Should open in Stata 13
foreach data of local converted_datasets {
	cap use `rootdir'/`data'.dta, clear
	assert _rc==0
}

log close
