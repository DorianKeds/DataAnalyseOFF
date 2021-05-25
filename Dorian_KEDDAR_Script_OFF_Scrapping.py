#!/usr/bin/env python
# coding: utf-8

# In[49]:


# ----------- Import --------------
import pandas as pd
import requests
from bs4 import BeautifulSoup
import random
import time

# ----------- Global Viariable Init --------------
n = list(range(1,7980,1)) #Number of pages to be scraped
url_OFF = "https://fr.openfoodfacts.org/" #Url of the Open Food Fact website

# |----------- url_scrap function ---------------|
# |----------------- Definition -----------------|
# |  The url_scrap function allows to get the    |
# |   ulrs of the products                       |
# |------------------- author -------------------|
# | Dorian KEDDAR - 03/05/2021                   |
# |----------------------------------------------|
def url_scrap():
    pages_url = []
    urls = []
    product_url = []
    start_time = time.time() #Timer start
    # I get the urls of the pages from 1 to 7990
    for i in range(len(n)):
        page_url = url_OFF + str(n[i])
        pages_url.append(page_url)
    # I get the URLS of the products present on the pages
    for i in range(len(pages_url)):
        html = requests.get(pages_url[i]).text
        soup = BeautifulSoup(html , "html.parser")
        a = soup.find('div', attrs={'id':'search_results'}).find_all('a')
        for i in range(len(a)):
            href = a[i]['href']
            product_url.append(href)
    #I add the urls of the pages with the url of the products
    for j in range(len(product_url)):
        u = url_OFF + product_url[j]
        urls.append(u)
    print("--- %s seconds execution for urls collect ---" % (time.time() - start_time)) #Display the execution time for the url_scapt function
    return urls


# |----------- scrap_info function --------------|
# |----------------- Definition -----------------|
# | The scrap_info function allows you to        |
# | retrieve the information of each product     |
# |------------------- author -------------------|
# | Dorian KEDDAR - 03/05/2021                   |
# |----------------------------------------------|
def scrap_info():
    infos = []
    url = url_scrap()
    start_time = time.time()
    for i in range(len(url)):
        html = requests.get(url[i]).text
        soup = BeautifulSoup(html, 'html.parser')

# Product_Name 
        name = soup.find('h1', attrs = {'itemprop':'name'})
        if name:
            name = name.contents[0]
        else:
            name = "XXX"
# Barcode
        code = soup.find('span', attrs = {'itemprop':'gtin13'})
        if code:
            code = code.contents[0]
        else:
            code = "XXX"
#--------------------------- Products Caracteristique ---------------------------#

        cara_prod =  soup.find_all('div', attrs = {'class':'medium-12 large-8 xlarge-8 xxlarge-8 columns'})
        p = cara_prod[0].find_all('p')

# Product description        
        try:
            desc = soup.find('span', attrs = {'itemprop':'description'}).contents[0] 
        except:
            desc = "XXX"
# Quantity
        try:
            quant = p[1].text[10:].strip()
        except:
            quant = 'XXX'
#Packaging
        try:
            condi = p[2].text[17:].strip()
        except:
            condi = 'XXX'
#Brands
        brand = cara_prod[0].find_all('a', attrs = {'itemprop':'brand'})
        for i in range(len(brand)):
            b = brand[i].text[0:]
#Categories
        try:
            c = soup.select('a[href*=categorie]')
        except:
            c = 'XXX'
#Labels
        try:
            label = soup.select('a[href*=label]')
        except:
            label = 'XXX'
#Origin
        try:
            ori = soup.select('a[href*=origine]')
        except:
            ori = 'XXX'
#Production_palce
        try:
            fab_pla = soup.select('a[href*=lieu-de-fabrication]')
        except:
            fab_pla = 'XXX'
#Tracking_code
        try:
            c_trac = soup.select('a[href*=code-emballeur]')
        except:
            c_trac = 'XXX'
#Stores
        try:
            store = soup.select('a[href*=magasin]')
        except:
            store = 'XXX'
#Sales_countries
        try:
             sale= soup.select('a[href*=pays]')
        except:
            sale = 'XXX'
# Ingredients
        ing = soup.find('div', attrs = {'id':'ingredients_list'})
        if ing:
            ing = ing.text[0:].strip()
        else:
            ing = 'XXX'
               
            
#--------------------------- Nutritionnals Values ---------------------------#
#Energy Value per 100g (in kj)
        nrj100 = soup.find('tr', attrs = {'id':'nutriment_energy-kj_tr'}).find_all('td', attrs = {'class':'nutriment_value'})
        if nrj100:
            nrj100 = nrj100[0].text[0:].strip()
            if nrj100 == '?':
                nrj100 = 'XXX'
        else:
            nrj100 = 'XXX'
            
#Comparative Energy Value per 100g (in kj)
        nrj100c = soup.find('tr', attrs = {'id':'nutriment_energy-kj_tr'}).find('span', attrs = {'class':'compare_value'})
        if nrj100c:
            nrj100c = nrj100c.text[0:].strip()
            if nrj100c == '?':
                nrj100c = 'XXX'
        else:
            nrj100c  = 'XXX'
            
#Energy Value per 100g (in kcal)
        nkcal100 = soup.find('tr', attrs = {'id':'nutriment_energy-kcal_tr'}).find_all('td', attrs = {'class':'nutriment_value'})
        if nkcal100:
            nkcal100 = nkcal100[0].text[0:].strip()
            if nkcal100 == '?':
                nkcal100 = 'XXX'
        else:
            nkcal100 = 'XXX'
            
#Comparative Energy Value per 100g (in kcal)
        nkcal100c = soup.find('tr', attrs = {'id':'nutriment_energy-kcal_tr'}).find('span', attrs = {'class':'compare_value'})
        if nkcal100c:
            nkcal100c = nkcal100c.text[0:].strip()
            if nkcal100c == '?':
                nkcal100c = 'XXX'
        else:
            nkcal100c = 'XXX'
#Fat Value
        mat_gr = soup.find('tr', attrs={'id':'nutriment_fat_tr'}).find_all('td', attrs={'class':'nutriment_value'})
        if mat_gr:
            mat_gr = mat_gr[0].contents[0].strip()
            if mat_gr == "?":
                mat_gr = "XXX"
        else:
            mat_gr = "XXX"
            
#Comparative Fat Value
        mat_grc = soup.find('tr', attrs={'id':'nutriment_fat_tr'}).find('span', attrs = {'class':'compare_value'})
        if mat_grc:
            mat_grc = mat_grc.contents[0].strip()
            if mat_grc == "?":
                mat_grc = "XXX"
        else:
            mat_grc = "XXX"

#Saturated Fatty Acid Value 
        acide = soup.find('tr', attrs = {'id':'nutriment_saturated-fat_tr'})
        if acide:
            acide = acide.find_all('td', attrs={'class':'nutriment_value'})
            if acide:
                acide = acide[0].contents[0].strip()
                if acide == "?":
                    acide = "XXX"
            else:
                acide = "XXX"

#Comparative Saturated Fatty Acid Value
        acide_c = soup.find('tr', attrs = {'id':'nutriment_saturated-fat_tr'})
        if acide_c:
            acide_c = acide_c.find('span', attrs = {'class':'compare_value'})
            if acide_c:
                acide_c = acide_c.contents[0].strip()
                if acide_c == "?":
                    acide_c = "XXX"
            else:
                acide_c = "XXX"
#Sugar Value
        su = soup.find('tr', attrs = {'id':'nutriment_sugars_tr'})        
        if su:
            su = su.find_all('td', attrs={'class':'nutriment_value'})
            if su:
                su = su[0].contents[0].strip()
                if su == "?":
                    su = "XXX"
            else:
                su = "XXX"
                
#Comparative Sugar Value
        su_c = soup.find('tr', attrs = {'id':'nutriment_sugars_tr'})        
        if su_c:
            su_c = su_c.find('span', attrs = {'class':'compare_value'})
            if su_c:
                su_c = su_c.contents[0].strip()
                if su_c == "?":
                    su_c = "XXX"
            else:
                su_c = "XXX"
#Sodium Value 
        so = soup.find('tr', attrs = {'id':'nutriment_sodium_tr'})
        if so:
            so = so.find_all('td', attrs={'class':'nutriment_value'})
            if so:
                so = so[0].contents[0].strip()
                if so == "?":
                    so = "XXX"
            else:
                so = "XXX"

#Comparative Sodium Value
        so_c = soup.find('tr', attrs = {'id':'nutriment_sodium_tr'})
        if so_c:
            so_c = so_c.find('span', attrs = {'class':'compare_value'})
            if so_c:
                so_c = so_c.contents[0].strip()
                if so_c == "?":
                    so_c = "XXX"
            else:
                so_c = "XXX"                
                
#Nutri_Score
        nu = soup.find('tr', attrs = {'id':'nutriment_nutriscore_tr'})
        if nu:
            nu = nu.find_all('td', attrs={'class':'nutriment_value'})
            if nu:
                nu = nu[0].contents[0].strip()
                if nu == "?":
                    nu = "XXX"
            else:
                nu = "XXX"
#Nova_Score
        try:
            nova = soup.select('img[src*=nova-group]')[0]['alt']
        except:
            nova = 'XXX'
#Eco_Score
        try:
            eco_score = soup.select('img[src*=ecoscore]')[1]['alt']
        except:
            eco_score = 'XXX'
# Ingredient analysis
        try:
             additif = soup.select('a[href*=additif]')
        except:
            additif = 'XXX'
        try:
             palm = soup.select('a[href*=ingredients-issus-de-l-huile-de-palme]')
        except:
            palm = 'XXX'

#--------------------------- Add on list and transform list in DataFrame ---------------------------#      
        infos.append((name,code, nu, desc, quant, condi, b, c, label, ori, fab_pla, c_trac, store, sale, ing, nrj100, nrj100c, nkcal100, nkcal100c, mat_gr, mat_grc, acide,acide_c, su, su_c, so, so_c, nova, eco_score, additif, palm))
        df = pd.DataFrame(infos, columns = ['Product_Name', 'Barcode', 'Nutri_Score', 
                                        'Description','Quantity', 'Packaging', 'Brands', 'Categories', 'Label', 'Origin', 
                                        'Production_places', 'Tracking_code', 'Stores', 'Sales_countries','Ingredients', 
                                        'Energie(KJ)_100',  'Energie(KJ)_100_compar', 'Energie(Kcal)_100',
                                        'Energie(Kcal)_100_Compar', 'Fat_Value', 'Fat_Value_Compar','Saturated_Fatty_Acid_Value', 
                                        'Saturated_Fatty_Acid_Value_Compar', 'Sugar_Value', 'Sugar_Value_Compar', 'Sodium_Value', 
                                        'Sodium_Value_Compare', 'Nova_Score', 'Eco_Score', 'Additives', 'Palm_Oil_Ingredient'])
    print("--- %s seconds execution for data collect ---" % (time.time() - start_time))
    return df

# |----------- csv_extract function -------------|
# |----------------- Definition -----------------|
# | The scrap_info function allows to            |
# | extract in csv format the obtained DataFrame |
# |------------------- author -------------------|
# | Dorian KEDDAR - 03/05/2021                   |
# |----------------------------------------------|
def csv_extract():
    df = scrap_info()
    df.to_csv('OFF_Products.csv')

