txt2macro manifest.txt
local datasets `r(mymacro)'

local dir D:/wbStata/datasets/
foreach data of local datasets {
	cap sysuse "`data'", clear
	if _rc == 0 {
		save "`dir'/`data'.dta", replace
	}
}
