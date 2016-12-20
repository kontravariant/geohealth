library(RSQLite)
library(reshape)
#connect to country_data
db = dbConnect(SQLite(), 'data/country_data.sqlite')
#pull table names, escape in quotes
cnames = dbListTables(db)
tbl_name = sapply(cnames, function(x) paste('"',x,'"',sep = ""))
#list out tables named with ISO Alpah3
tbl = list(); tbl = lapply(tbl_name, function(x) tbl[x] = dbReadTable(db,x))
name = cnames[cnames=='ALB']
usa = tbl[[name]]
usa.molten = melt(usa, id='Statistic', variable_name = "year")
usa.cast = cast(usa.molten, year~Statistic)
usa.cast$country=paste(name)
