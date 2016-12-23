library(RSQLite)
library(dplyr)
#read in csv of income codes
raw.dat = read.csv("data/country_info/income_codes.csv")
#rename code to country
colnames(raw.dat)[1] = 'country'
#get all country names and find which ones are not income coded
db = dbConnect(SQLite(), "data/country_data.sqlite")
tableList = dbListTables(db)
panel = dbReadTable(db,"PANEL")
#list of all countries that are income-coded
coded.countries = as.character(raw.dat$Code)
#dif is list of non-coded countries that we have data for, ignoring 'PANEL'
dif = setdiff(tableList,coded.countries)
join.dat = raw.dat[,c('country','Income.code')]

#left join the codes onto the panel data by country and if the data frame
#sizes match then overwrite the panel data in the databse.
binded = left_join(panel,join.dat,by='country')
if(nrow(panel) == nrow(binded)){
  dbWriteTable(db,'PANEL',binded,overwrite=TRUE)
}

