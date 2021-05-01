import requests
import gzip
import xml
import codecs
import re

import pandas as pd

from tqdm import tqdm
from html_table_extractor.extractor import Extractor
from bs4 import BeautifulSoup


class Data_FincaRaiz:
    def __init__(self):
        return None
    
    def get_sitemap():
        """[summary]
        """
        url =  'https://www.fincaraiz.com.co/sitemaps/SiteMap_Index.xml'
        response = requests.get(url)
        s = BeautifulSoup(response.text, 'lxml')
        links_html = s.find('sitemapindex').find_all('loc')
        links = [links.get_text()  for links in links_html]
        response = requests.get(links[0])
        r = requests.get(links[0], allow_redirects=True)
        open('1.xml.gz', 'wb').write(r.content)

        with gzip.open("1.xml.gz", "rb") as f:
            data = f.read()
            
        s = BeautifulSoup(data, "lxml")
        reviews = s.find('urlset',attrs={'class':''}).find_all('loc',attrs={'class':''})
        reviews_list = [links.get_text() for links in reviews]
        
        return(reviews_list)

    def filter_by_words(word,reviews_list):
        """[summary]

        Args:
            word ([type]): [description]
            reviews_list ([type]): [description]

        Returns:
            [type]: [description]
        """
        if any(word in w for w in reviews_list):
            bogota = [s for s in reviews_list if word in s]
        return (bogota)

#data proyect
    def project_name(s):
        """[summary]

        Args:
            s ([type]): [description]
        """
        project_name = s.find('div',attrs={'class':'row detailContent'}).find_all('h1',attrs={'style':'margin-bottom: 0px; line-height: 95%;'})
        project_name = [w.get_text() for w in project_name]
        return(project_name)

    def project_zone(s):
        """[summary]

        Args:
            s ([type]): [description]
        """
        project_zone = s.find('div',attrs={'class':'row detailContent'}).find_all('span',attrs={'class':'font-light'})
        project_zone = [w.get_text() for w in project_zone]
        return(project_zone)

    def project_addres(s):
        """[summary]

        Args:
            s ([type]): [description]
        """
        project_addres = s.find('div',attrs={'class':'row detailContent'}).find_all('span',attrs={'class':'address'})
        project_addres = [w.get_text() for w in project_addres]
        return(project_addres)  

    def project_owner(s):
        """[summary]

        Args:
            s ([type]): [description]
        """
        project_owner = s.find('div',attrs={'class':'contact-form'}).find('div',attrs={'class':'tCenter'}).find_all('a',attrs={'class':''})
        project_owner = [w.get_text() for w in project_owner]
        project_owner = project_owner[1]
        return(project_owner)    

    def project_estrato(s):
        """[summary]

        Args:
            s ([type]): [description]
        """
        project_estrato = s.find('div',attrs={'class':'row features_2 '}).find('ul',attrs={'class':'boxcube'}).find_all('li',attrs={'class':''})
        project_estrato = [w.get_text() for w in project_estrato]
        a=project_estrato[2]
        project_estrato=[int(s) for s in a.split() if s.isdigit()]
        return(project_estrato)

    def data_table(s):
        """[summary]

        Args:
            s ([type]): [description]
        """
        table_doc = s.find_all('table')
        extractor = Extractor(table_doc[0])
        extractor = extractor.parse()
        tabla = extractor.return_list()
        tabla_columns = tabla[0]
        tabla_datos = tabla[1:]
        final = []
        for fila in tabla_datos:
            for element in fila:
                a = [w.strip() for w in fila]
                final.append(a)        
        df = pd.DataFrame(final, columns = tabla_columns)
        return(df)
    
    def extraction():
        project_name = Data_FincaRaiz.project_name(s)
        project_zone = Data_FincaRaiz.project_zone(s)
        project_addres = Data_FincaRaiz.project_addres(s)
        project_owner = Data_FincaRaiz.project_owner(s)
        project_estrato = Data_FincaRaiz.project_estrato(s)
        data_table = Data_FincaRaiz.data_table(s)

        return(project_name, project_zone, project_addres, project_owner, project_estrato, data_table)
    
    def compute(self):
        """[summary]
        """
      
        sitetmap = Data_FincaRaiz.get_sitemap()
        bogota = Data_FincaRaiz.filter_by_words("bogota",sitetmap)
        bogota_proyecto_nuevo = Data_FincaRaiz.filter_by_words("proyecto-nuevo",bogota)
        
        print(len(bogota_proyecto_nuevo))

        for link in tqdm(bogota_proyecto_nuevo):
            print(link)
            response = requests.get(link)
            s = BeautifulSoup(response.text, 'lxml')
            
            if bool(re.search('Lo Sentimos, pero la página que busca no existe.', s.text)): 
                project_link = link
                project_status = "error"
                print("404")
                
            else:
                project_name, project_zone, project_addres, project_owner, project_estrato, data_table = Data_FincaRaiz.extraction()
                
        return(True)