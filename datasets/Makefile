.DEFAULT_GOAL := help

STATA_PATH="C:\Program Files (x86)\Stata13\StataMP-64"
EXECSTATA := $(STATA_PATH) -e do
DTA_ORIGIN := $(wildcard *.dta)
TESTOPEN_LOG := opentest-log.txt

.PHONY: getnick
getnick:
	wget -np -A ".dta" -np -nd -P out "https://github.com/NickCH-K/causaldata/tree/main/Stata/"


.PHONY: getdata
getdata: # Download all data
getdata: getdata.do manifest.txt txt2macro.ado
	@echo "+ $@"
	$(EXECSTATA) $<

$(TESTOPEN_LOG): # Log file for test opening of dta file in Stata
$(TESTOPEN_LOG): testopen.do $(DTA_ORIGIN)
	@echo "+ $@"
	$(EXECSTATA) $<	

testo: # Test opening of original Stata dta files
testo: $(TESTOPEN_LOG)
	@echo "+ $@"

testc: # Test opening of converted Stata dta files
testc: 
	@echo "+ $@"
	wbstata -t 13 -a 
	$(EXECSTATA) testopen-converted.do
	@find . -type f -name '*-wbstata*.dta' -exec rm -f {} +
	rm testopen.log testopen-converted.log

test: # Test opening of original & converted dta files
test: testo testc

.PHONY: check
check: # Print & check source do files
check: 
	@echo "+ test"
	@echo "+ "$(EXECSTATA)""
	@echo "+ $(DTA_ORIGIN)"

.PHONY: help
help: # Show Help
	@egrep -h '\s#\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?# "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'