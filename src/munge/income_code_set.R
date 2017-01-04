library(RSQLite)
library(dplyr)
#read in csv of income codes
raw.dat = read.csv("project/data/intermediate/country/income_codes.csv")
#rename columns
colnames(raw.dat) = c('country',"country code","income level","income code")
#get all country names and find which ones are not income coded
db = dbConnect(SQLite(), "project/data/processed/geohealth.sqlite")
tableList = dbListTables(db)
panel = dbReadTable(db,"PANEL")
#list of all countries that are income-coded
coded.countries = as.character(raw.dat$country)
#dif is list of non-coded countries that we have data for, ignoring 'PANEL'
dif = setdiff(tableList,coded.countries)
join.dat = raw.dat[,c('country code','income code')]

#left join the codes onto the panel data by country and if the data frame
#sizes match then overwrite the panel data in the databse.
binded = left_join(panel,join.dat,by=c('country'='country code'))
if(nrow(panel) == nrow(binded)){
  dbWriteTable(db,'PANEL',binded,overwrite=TRUE)
}

