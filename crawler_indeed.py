# -*- coding: utf-8 -*-
# Python3

import requests as rq
from bs4 import BeautifulSoup as bs
import json

BS_CONFIG = 'html5lib'
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:63.0) Gecko/20100101 Firefox/63.0'
MAIN_URL = "https://www.indeed.fr/jobs?"
LIMIT = 10

TAB_OFFRES = []

# https://www.indeed.fr/jobs?q=informatique&l=Montpellier+%2834%29&start=10

def get_all_pages(nbr_page,recherche,localisation):
    for page in range(0,nbr_page+1):
        if page == 0 :
            start = 0
        else :
            start = LIMIT * page
        url = MAIN_URL+'q='+str(recherche)+'&l='+localisation+'&start='+str(start)
        get_offres(url,recherche,localisation)

def get_offres(url,recherche,localisation):
    if ( recherche and localisation ):
        # q=informatique&l=Montpellier
        rep = rq.get(url, headers={'User-Agent': USER_AGENT})
        data = rep.text
        if data:
            soup = bs(data, BS_CONFIG)
            offres = soup.find_all('div' , 'jobsearch-SerpJobCard')
            for offre in offres:
                data_offre = {}
                if offre.find('a', 'jobtitle'):
                    data_offre["name"] = offre.find('a', 'jobtitle' ).text #Titre
                    link_title = offre.find('a', 'jobtitle' ) #Lien
                    data_offre["lien"] = 'https://www.indeed.fr'+link_title.get('href') #Lien
                    offre_complete = get_offre_complete(data_offre["lien"])
                    data_offre["description"] = offre_complete["description"]
                    data_offre["societe"] = offre_complete["societe"]
                    data_offre["salaire"] = offre_complete["salaire"]
                    TAB_OFFRES.append(data_offre)

def get_offre_complete(url):
    if url:
        rep = rq.get(url, headers={'User-Agent': USER_AGENT})
        data = rep.text
        if data:
            offre_complete = {}
            soup = bs(data, BS_CONFIG)
            offre = soup.find('div' , 'jobsearch-JobComponent')
            offre_complete["description"] = offre.find('div', 'jobsearch-JobComponent-description' ).text #Description
            if offre.find('div', 'jobsearch-InlineCompanyRating' ):
                offre_complete["societe"] = offre.find('div', 'jobsearch-InlineCompanyRating' ).findChild().text.upper() #Societe
            else:
                offre_complete["societe"] = ''
            if offre.find('div', 'jobsearch-JobMetadataHeader-item' ):
                infos_salaires = offre.find_all('div', 'jobsearch-JobMetadataHeader-item' ) #Salaire
                if len(infos_salaires) >= 2 :
                    offre_complete["salaire"] = infos_salaires[0].text
                else:
                    offre_complete["salaire"] = ''
            else:
                offre_complete["salaire"] = ''

            return offre_complete


###########################################
# LANCER LE SCRIPT
###########################################
get_all_pages(1,'informatique','Rennes')
###########################################
# LANCER LE SCRIPT
###########################################


with open('data-offres.json', 'w') as outfile:
    json.dump(TAB_OFFRES, outfile, indent=4 , ensure_ascii=False)
