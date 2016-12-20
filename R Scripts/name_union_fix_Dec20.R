library(gdata)
library(readstata13)
tbl =  read.csv("data/country_info/iso_wiki_tbl.csv")
map  = read.csv("data/country_info/country_map.csv")
pwt = read.dta13("data/Econ/pwt90.dta")
wiki = tbl$Country.name
map.names = map$ISO.Name
pwt.names = unique(pwt$country)
cdif = setdiff(x = wiki, y = map.names)
mdif = setdiff(map.names,pwt.names)
cat = sapply(map.names, function(x) as.character(x))
names = unique(c(cat,pwt.names))
alldiff = setdiff(wiki,names)
