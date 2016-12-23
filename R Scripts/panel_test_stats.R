library(RSQLite)
db = dbConnect(SQLite(), "data/country_data.sqlite")
tableList = dbListTables(db)
panel = dbReadTable(db,"PANEL")
countries = unique(panel$country)

#tests 
cty = 'USA'
subset = panel[panel$country==paste(cty),]
gdp.wtr = subset[c('year','rgdpe','water')]
gdp.wtr = gdp.wtr[(apply(gdp.wtr, 1, function(x) all(!is.na(x)))), ]
gdp = gdp.wtr$rgdpe
wtr = gdp.wtr$water
cor(gdp,wtr,use = "complete.obs")
