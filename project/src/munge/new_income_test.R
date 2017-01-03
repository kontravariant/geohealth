map = read_csv("project/data/country_map.csv")
coded = read_csv("project/data/intermediate/country/income_codes.csv")
dif = setdiff(map$`ISO Alpha3`,coded$`1`);print(dif)
