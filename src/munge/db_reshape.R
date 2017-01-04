library(RSQLite)
library(reshape)
library(dplyr)
library(readr)

#script call path (command line)
args <- commandArgs(trailingOnly = F)
scriptPath <- dirname(sub("--file=","",args[grep("--file",args)]))
print(scriptPath)

#source('.Rprofile')
#connect to country_data
dbpath = file.path(scriptPath,'../..','data/processed','geohealth.sqlite')
print(dbpath)
db = dbConnect(SQLite(), dbpath)
#pull table names, escape in quotes
cnames = dbListTables(db)
#ensure PANEL table is not included, as that is what we are creating here
cnames = cnames[cnames != 'PANEL']
#escape all names in quotes
tbl_name = sapply(cnames, function(x) paste('"',x,'"',sep = ""))
#list out tables
tbl = list(); tbl = lapply(seq_along(tbl_name), function(x,n,i) { tbl[x[i]] = dbReadTable(db,x[i]) }, x=cnames, n=tbl_name)
#name them with ISO Alpha3
names(tbl) = cnames


##REFORMAT TO LONG (cast by year, add country column)
#melt every country
tbl.molten = lapply(tbl, function(x) melt(x,id="Statistic",variable_name="year"))
#cast every country as long by year
tbl.cast = lapply(tbl.molten, function(x) cast(x,year~Statistic))

#get all names and create a column with each country name
namelist = cnames
tbl.cast.named = Map(cbind, tbl.cast, country=namelist)
#remove 'X' from every year i.e. X1950-->1950
tbl.cast.named.years = lapply(tbl.cast.named,
                    function(x) 
                    mutate(x, year=as.factor(
                    substring(
                    as.character(year),first = 3,last = nchar(as.character(year))))))
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
    #quick check if WDI::expend was in the data set, then manuall fix all numeric columns
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
stacked = col_format_stack(tbl.cast.named.years)



####################################
####################################
####join INCOME CODES to stacked data
####################################
#read in csv of income codes
raw.dat = read.csv("project/data/intermediate/country/income_codes.csv")
#rename columns
colnames(raw.dat) = c('country',"country code","income level","income code")
panel = stacked
join.dat = raw.dat[,c('country code','income code')]
#left join the codes onto the panel data by country and if the data frame
#sizes match then overwrite the panel data in the databse.
binded = left_join(panel,join.dat,by=c('country'='country code'))
if(nrow(panel) == nrow(binded)){
  dbWriteTable(db,'PANEL',binded,overwrite=TRUE)
} 


