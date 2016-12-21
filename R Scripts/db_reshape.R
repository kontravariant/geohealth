library(RSQLite)
library(reshape)
library(dplyr)
library(readr)
#connect to country_data
db = dbConnect(SQLite(), 'data/country_data.sqlite')
#pull table names, escape in quotes
cnames = dbListTables(db)
#ensure PANEL table is not included, as that is what we are creating here
cnames = cnames[cnames != 'PANEL']
#escape all names in quotes
tbl_name = sapply(cnames, function(x) paste('"',x,'"',sep = ""))
#list out tables named with ISO Alpha3
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
#function to stack the country panels
col_format_stack = function(casted) {
  #start null list
  tables.in = list()
  #get names of argument data sets in list
  named_names = names(casted)
  #for each data set
  for(i in 1:length(named_names)) {
    #use the name and log which one is beingworked on
    name = named_names[i]
    print(name)
    #get the ith tbale
    ctable = casted[[i]]
    #write as temp csv file, read back in using readr to get column types
    write_csv(ctable,"data/table.csv",col_names = TRUE)
    readin = readr::read_csv("data/table.csv")
    #quick check if expend was in the data set, then manuall fix all numeric columns
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
    #append current table to data list
    tables.in[[i]] = readin
  }
  #rbind all in list
  bound = bind_rows(tables.in)
  #return the bound data set panel
  return(bound)
}
#stack long country data sets into panel
binded = col_format_stack(tbl.cast.named.years)
#write stacked data sets
dbWriteTable(db,"PANEL",binded,overwrite=TRUE)


