SHELL:=/usr/bin/env bash

rebuild: clean tree run

clean:
	@echo "-->RESETTING: deleting file tree to bare"
	@rm -rf data/intermediate data/processed data/raw
	@rm -f data/table.csv
	@rm -f gecko*
	@rm -f *~
	@rm -rf models
	@rm -rf reports
	@echo "-->NOTE: data/country_map.csv is 'sacred' like 'src'!"

tree: 
	@echo "-->Filling out directory tree"
	@mkdir data/intermediate data/intermediate/country data/intermediate/pwt data/intermediate/wdi data/intermediate/who
	@mkdir -p data/raw data/raw/country data/raw/pwt data/raw/wdi data/raw/who
	@mkdir data/processed
	@mkdir -p reports/graphics
	@mkdir models
	@echo "-->File tree created!"
run:
	@echo "-->Getting data, THEN Munging data!"
	@python src/autorun.py
	@echo "-->Panel data is present in data/processed/geohealth.sqlite > PANEL"
	@echo "-->geckodriver.log is selenium web driver log, useless unless your data is bad (someone changed their website!)"
	@rm -rf *~
	@echo "-->SQLite Database produced, PANEL data present"

