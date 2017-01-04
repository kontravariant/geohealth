from munge import who_munge,wdi_munge,pwt_munge,data_collate,db_write_collated,income_parse

def munge_all():
    #munge three into intermediate
    print("Shaping WHO Data")
    who_munge.who_munge()
    print("Shaping WDI Data")
    wdi_munge.wdi_munge()
    print("Shaping PWT Data")
    pwt_munge.pwt_munge()
    #process intermediate
    print("Collating all, then pickling")
    data_collate.collate_and_pickle()
    #write to sqlite
    print("Writing SQLite Database of countryframes")
    db_write_collated.write_db()


    #income code parser
    print("Parsing income codes to map")
    income_parse.income_code_parser()

if __name__ == "__main__":
    print("Munging all")
    munge_all()