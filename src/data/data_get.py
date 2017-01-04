#get health (wdi, who) and econ data
import requests
from bs4 import BeautifulSoup as bs
import os

from selenium import webdriver
import urllib.request, urllib.parse

import re

import zipfile
import pandas as pd

datadir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../../', 'data/'))

#download immunization csv files from who.int
def who_get():
    data_page_link = "http://apps.who.int/gho/data/node.main.A824?lang=en"
    site_link = data_page_link.rsplit('node', 1)[0]
    top_site_link = data_page_link.rsplit('data/node',1)[0]
    print(site_link)
    data_page_req = requests.get(data_page_link)
    data_links = []
    if data_page_req.status_code == 200:
        top_soup = bs(data_page_req.text,'html.parser')
        print('success @ {}'.format(top_soup.title.string))
        for li in top_soup.find("ul", {'class':'list_dash'}).find_all("li"):
            childs = li.find_all("a")
            for child in childs:
                node_link = child['href']
                current_link = site_link+node_link
                data_links.append(current_link)
    else:
        print(data_page_req.status_code)

    for page in data_links:
        driver = webdriver.Firefox()
        driver.get(page)
        page_title = driver.title
        res = re.search("r(.*?\|\ )(.*)(\ -)", page_title)
        stat = res.group(2)
        driver.switch_to.frame(driver.find_element_by_id("content_iframe"))
        driver.switch_to.frame(driver.find_element_by_id("passthrough"))
        aes = driver.find_elements_by_xpath("//a[contains(@class, 'control')]")[1]
        lnk = aes.get_attribute('href')
        print(lnk)
        urllib.request.urlretrieve(lnk,os.path.join(datadir+'/raw/who/{}.csv'.format(stat)))
        print(stat)
        driver.quit()

def wdi_get():

    top_url = "http://data.worldbank.org/data-catalog/world-development-indicators"
    driver = webdriver.Firefox()
    driver.get(top_url)
    aref = driver.find_element_by_xpath("//a[contains(@data-reactid,'196')]")
    href = aref.get_attribute('href')

    fdir = os.path.join(datadir,'raw/wdi/')

    fpath = fdir+'wdi.zip'
    urllib.request.urlretrieve(href,fpath)
    driver.quit()
    zip_ref = zipfile.ZipFile(fpath, 'r')
    zip_ref.extractall(fdir)
    zip_ref.close()
    os.remove(fpath)


def pwt_get():
    dta_url = "http://www.rug.nl/ggdc/docs/pwt90.dta"
    split_url = urllib.parse.urlsplit(dta_url)
    filename = os.path.join(datadir,"raw/pwt/",split_url.path.split("/")[-1])
    urllib.request.urlretrieve(dta_url, filename)

def cdata_get():
    income_xls_url = "http://databank.worldbank.org/data/download/site-content/CLASS.xls"
    split_url = urllib.parse.urlsplit(income_xls_url)
    filename = os.path.join(datadir,"raw/country/",split_url.path.split("/")[-1])
    urllib.request.urlretrieve(income_xls_url, filename)

def get_all():
    who_get()
    wdi_get()
    pwt_get()
    cdata_get()

if __name__ == "__main__":
    get_all()
