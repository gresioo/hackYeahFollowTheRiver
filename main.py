'''
Created on 27 lis 2020

@author: obi1i
'''

import googlesearch 
import requests  
import re
import time
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import urllib
from validate_email import validate_email

from selenium import webdriver
import selenium
from inscriptis import get_text 

#format data validation methods
def ACCOUNT_val(data_in):
    if len(data_in) == 0 or data_in == ('',''):
        return_value = False
    else:
        return_value = True
    return return_value 

def NIP_val(data_in):
    if len(data_in) == 0 or data_in == ('',''):
        return_value = False
    else:
        return_value = True
    return return_value 

def REGON_val(data_in):
    if len(data_in) == 0 or data_in == ('',''):
        return_value = False
    else:
        weights = [8, 9, 2, 3, 4, 5, 6, 7]
        numbers = [int(x) for x in data_in]
        multi = [x*y for (x,y) in zip(weights,numbers)]
        x = sum(multi) % 11
        if x == 10:
            x = 0
        if numbers[8] == x:
            return_value = True
        else:
            return_value = False
    return return_value 

def PHONE_SHORT_val(data_in):
    if len(data_in) == 0 or data_in == ('',''):
        return_value = False
    else:
        return_value = True
    return return_value 

def PHONE_LONG_val(data_in):
    if len(data_in) == 0 or data_in == ('',''):
        return_value = False
    else:
        return_value = True
    return return_value 

def PHONE_LONG_PL_val(data_in):
    if len(data_in) == 0 or data_in == ('',''):
        return_value = False
    else:
        return_value = True
    return return_value 

def EMAIL_val(data_in):
    if len(data_in) == 0 or data_in == ('',''):
        return_value = False
    else:
        return_value = True
    return return_value 

def POST_CODE_val(data_in):
    if len(data_in) == 0 or data_in == ('',''):
        return_value = False
    else:
        return_value = True
    return return_value 

#data post processing functions
def EMAIL_post(data_in,vector_name):
    return([vector_name[0], data_in.split('@')[0]])

#vector type processing functions

def ACCOUNT_process(data):
    print(data)

def NIP_process(data):
    print(data)
    
def REGON_process(data):
    print(data)
    
def PHONE_SHORT_process(data):
    print(data)
    
def PHONE_LONG_process(data):
    print(data)
    
def EMAIL_process(data):
    print(data)
    
def POST_CODE_process(data):
    print(data)

def NICK_process(data):
    print(data)

regexp_definition = [
['ACCOUNT',"\d{2}[ ]\d{4}[ ]\d{4}[ ]\d{4}[ ]\d{4}[ ]\d{4}[ ]\d{4}"],
['NIP',"[0-9]{3}-[0-9]{3}-[0-9]{2}-[0-9]{2}"],
['REGON',"[0-9]{9}"],
['REGON',"[0-9]{14}"],
['PHONE_SHORT',"[ \"]([1-9][0-9]{8})[ \"]"],
['PHONE_SHORT',"[1-9][0-9]{2}[-\. ][0-9]{3}[-\. ][0-9]{3}"],
['PHONE_LONG',"((\+|00)[1-9][0-9]{0,3})?[1-9][0-9]{8}"],
['PHONE_LONG_PL',"((\+|00)48)?[1-9][0-9]{8}"],
['EMAIL',"[a-zA-Z0-9\._]+@[a-zA-Z0-9.]+\.[a-zA-Z0-9]+",['NICK']],
['POST_CODE',"[0-9]{2}-[0-9]{3}"]]

def check_all_regexps(data,output_data,what_to_add):

    for reg_exp_item in regexp_definition:
        results = re.findall(reg_exp_item[1],data)
        for result in results:
            if globals()[reg_exp_item[0]+"_val"](result):
                output_data.append({'key': result, 'value': reg_exp_item[0], 'where_found': what_to_add})
            # if reg_exp_item[0]+"_post" in globals():
            #     new_vectors = globals()[reg_exp_item[0]+"_post"](result,reg_exp_item[2])
            #     results = re.findall(new_vectors[1].replace('.','\\.'),data)
            #     output_data.update({new_vectors[1]:[new_vectors[0],len(results)]})
    return output_data
        
#parameters
number_of_iteration = 1
number_of_results_per_iteration = 3 
query = "KOTY ROSYJSKIE"


'''
f = open("test_file.txt","r")
file_in = f.read()

out = check_all_regexps(file_in)
print(out)
'''
#global database
global_output_vectors = []


def search_engine(phrase, results_no,local_output_vectors):
    browser = webdriver.Firefox()
    try:
        list_of_pages_gen = googlesearch.search(phrase, tld="com", num=results_no, stop=results_no, pause=5)
    except Exception as ex:
        print("HTTP Error:",ex)
    finally:
   
    # list_of_pages = ["https://www.olx.pl/oferty/q-koty-rosyjskie/",
    # #     #              "https://www.olx.pl/oferta/tanio-iphone-6-plus-128gb-super-stan-CID99-IDGRvIq.html#b4642646e3",
    # #     #              "https://allegrolokalnie.pl/oferta/iphone-8-64-gb-zloty-tanio",
    # #     #              "https://www.twoj-smartfon.pl/pl/p/Iphone-11-64-GBCzarnyPL-DystrybucjaGwarancja-producentaWysylka-24HPOLSKI-SKLEP/1243"
                     
    #      ]
    # if True:
        list_of_pages = [x for x in list_of_pages_gen]
        
        for url_item in list_of_pages:
            
            #URL data extraction
            url_scheme = urlparse(url_item).scheme
            url_domain = urlparse(url_item).netloc
            url_path = urlparse(url_item).path
            url_parameters = urlparse(url_item).params
            url_query = urlparse(url_item).query
            print(url_item)
            #URL rebuild
            url_full = url_scheme+"://"+url_domain+url_path 
            
            if url_domain == "olx.pl" or url_domain == "www.olx.pl":
                
                    
                browser.get(url_full)
                if not 'oferta' in url_full:  #list of pages... crawl it
                    alllinks=browser.find_elements_by_tag_name('a')
                    for link in alllinks:
                        linkaddress=link.get_attribute('href')
                        try:
                            if not linkaddress in list_of_pages:
                                if 'oferta' in linkaddress: #link do pojedynczej oferty
                                    list_of_pages.append(linkaddress)
                                elif 'oferty' in linkaddress: #link do następnej podstrony
                                    list_of_pages.append(linkaddress)
                        except TypeError: #jeśli nie ma hrefa (podobno się zdarzyło)
                            pass
                try:
                    browser.find_element_by_id("contact_methods_below").click()
                except selenium.common.exceptions.NoSuchElementException:
                    pass
                except selenium.common.exceptions.ElementClickInterceptedException:
                    browser.find_element_by_id("onetrust-accept-btn-handler").click()
                    browser.find_element_by_id("contact_methods_below").click()
                except selenium.common.exceptions.ElementNotInteractableException:
                    pass
                time.sleep(0.5)
                source_to_check = get_text(browser.page_source)
                # browser.close()
            elif url_domain == "allegro.pl":
                browser = webdriver.Firefox()
                browser.get(url_full+"#aboutSeller")
        
                #soup = BeautifulSoup(browser.page_source, 'html.parser')
                #results = soup.find('section','_sizcr _1xzdi _ai5yc _1vzz9 _ku8d6 _1o9j9 _1yx73 _1k7mg _10a7o')
                
                source_to_check = get_text(browser.page_source)
                # browser.close()
            else:
                pass
                static_html = requests.get(url_full)
                source_to_check = get_text(static_html.content.decode('utf-8'))

            local_output_vectors = check_all_regexps(source_to_check, local_output_vectors,url_domain+url_path)
        
        browser.close()
        return local_output_vectors
        
global_output_vectors = search_engine(query, number_of_results_per_iteration, global_output_vectors)

print(global_output_vectors)

#create variants
#tbd - i.e. take nip value and create version without - or with .

outputDf=pd.DataFrame(global_output_vectors)
outputDf=outputDf.drop_duplicates(ignore_index=True)
XLSXwriter=pd.ExcelWriter('output.xlsx')
outputDf.groupby('key').count()['value'].to_excel(XLSXwriter,sheet_name='Summary',columns=['Number of repetitions'])
outputDf.to_excel(XLSXwriter,sheet_name='All data')
XLSXwriter.save()


for iteration_index in range(2,1+number_of_iteration):
    print("Iteration level: ",iteration_index)
    for item in global_output_vectors:
        vector = global_output_vectors[item][0]
        globals()[vector+"_process"](item)

     
