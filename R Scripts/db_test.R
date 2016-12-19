require(RSQLite)
db = dbConnect(SQLite(), 'data/country_data.sqlite')
tlist = dbListTables(db)
ctest = tlist[1]
for(code in tlist){
  tbl = dbReadTable(db,paste(code))
  if(is.na(tbl[14,'X2013'])){
    print(code)
  }
}

