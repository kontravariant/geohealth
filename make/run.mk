run:
	@echo "-->Getting data, THEN Munging data!"
	@python src/autorun.py
	@echo "-->Panel data is present in data/processed/geohealth.sqlite > PANEL"
	@echo "-->geckodriver.log is selenium web driver log, useless unless your data is bad (someone changed their website!)"
	@rm -rf *~
	@echo "-->SQLite Database produced, PANEL data present"
