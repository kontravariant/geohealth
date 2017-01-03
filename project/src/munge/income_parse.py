import pandas as pd
import xlrd

def income_code_parser():
    dat = pd.read_excel('../../data/raw/country/CLASS.xls',)
    wb = xlrd.open_workbook('../../data/raw/country/CLASS.xls')
    sheet = wb.sheet_by_index(0)
    names = sheet.col_values(2,6,224)
    countries = sheet.col_values(3,6,224)
    incomes = sheet.col_values(6,6,224)
    dict = list(zip(names,countries, incomes))
    df = pd.DataFrame(dict)
    code_map = {
        'Low income':'LOI',
        'Lower middle income':'LMI',
        'Upper middle income':'UMI',
        'High income':'HII'
    }
    df[3] = df[2].map(code_map)
    #fix Andorra, Dem Rep Congo, Romania, Timor-Leste
    df.loc[df[1] == 'ADO',1] = 'AND'
    df.loc[df[1] == 'ZAR',1] = 'COD'
    df.loc[df[1] == 'ROM',1] = 'ROU'
    df.loc[df[1] == 'TMP',1] = 'TLS'
    df.to_csv('../../data/intermediate/country/income_codes.csv',index=False)

if __name__ == "__main__":
    income_code_parser()