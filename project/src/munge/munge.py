import who_munge,wdi_munge,pwt_munge,data_collate,db_write_collated
import income_parse

if __name__ == "__main__":
    #munge three into intermediate
    who_munge.who_munge()
    wdi_munge.wdi_munge()
    pwt_munge.pwt_munge()
    #process intermediate
    data_collate.collate_and_pickle()
    #write to sqlite
    db_write_collated.write_db()


    #income code parser
    income_parse.income_code_parser()




