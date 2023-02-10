local datasets auto auto2 bplong cancer census citytemp educ99gdp gnp96 lifeexp
local datasets `datasets' nlsw88 pop2000 sp500 uslifeexp uslifeexp2 voter

local dir D:/wbStata/datasets/
foreach data of local datasets {
	cap sysuse "`data'", clear
	if _rc == 0 {
		save "`dir'/`data'.dta", replace
	}
}