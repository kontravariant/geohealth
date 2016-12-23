library(RSQLite)
db = dbConnect(SQLite(), "data/country_data.sqlite")
tableList = dbListTables(db)
panel = dbReadTable(db,"PANEL")
countries = unique(panel$country)

