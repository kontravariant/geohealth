clean:
	@echo "-->RESETTING: deleting file tree to bare"
	@rm -rf data/intermediate data/processed data/raw
	@rm -f data/table.csv
	@rm -f gecko*
	@rm -f *~
	@rm -rf models
	@rm -rf reports
	@echo "-->NOTE: data/country_map.csv is 'sacred' like 'src'!"
