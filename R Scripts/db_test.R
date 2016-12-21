library(RSQLite)
library(reshape)
library(dplyr)
library(readr)
#connect to country_data
db = dbConnect(SQLite(), 'data/country_data.sqlite')
#pull table names, escape in quotes
cnames = dbListTables(db)
tbl_name = sapply(cnames, function(x) paste('"',x,'"',sep = ""))
#list out tables named with ISO Alpah3
tbl = list(); tbl = lapply(tbl_name, function(x) tbl[x] = dbReadTable(db,x))

##REFORMAT TO LONG (cast by year, add country column)
#melt every country
tbl.molten = lapply(tbl, function(x) melt(x,id="Statistic",variable_name="year"))
#cast every country as long by year
tbl.cast = lapply(tbl.molten, function(x) cast(x,year~Statistic))
#get all names and create a column with each country name
namelist = names(tbl.cast)
tbl.cast.named = Map(cbind, tbl.cast, country=namelist)
#remove 'X' from every year i.e. X1950-->1950
tbl.cast.named.years = lapply(tbl.cast.named,
                              function(x) 
                                mutate(x, year=as.factor(
                                  substring(
                                    as.character(year),first = 2,last = nchar(as.character(year))))))
col_format_stack = function(casted) {
  tables.in = list()
  named_names = names(casted)
  for(i in 1:length(named_names)) {
    name = named_names[i]
    print(name)
    ctable = casted[[i]]
    write_csv(ctable,"data/table.csv",col_names = TRUE)
    readin = readr::read_csv("data/table.csv")
    if("expend" %in% colnames(readin))
    {
      readin$expend = as.numeric(readin$expend);
      readin$hc = as.numeric(readin$hc);
      readin$statcap = as.numeric(readin$statcap);
      readin$avh = as.numeric(readin$avh);
      readin$ctfp = as.numeric(readin$ctfp);
      readin$cwtfp = as.numeric(readin$cwtfp);
      readin$rtfpna = as.numeric(readin$rtfpna);
      readin$rwtfpna = as.numeric(readin$rwtfpna);
    }
    tables.in[[i]] = readin
  }
  bound = bind_rows(tables.in)
  return(bound)
}
binded = col_format_stack(tbl.cast.named.years)



