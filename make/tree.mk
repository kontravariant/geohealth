tree: 
	@echo "-->Filling out directory tree"
	@mkdir data/intermediate data/intermediate/country data/intermediate/pwt data/intermediate/wdi data/intermediate/who
	@mkdir -p data/raw data/raw/country data/raw/pwt data/raw/wdi data/raw/who
	@mkdir data/processed
	@mkdir -p reports/graphics
	@mkdir models
	@echo "-->File tree created!"
