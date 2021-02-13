import requests
from bs4 import BeautifulSoup
import gzip
import xml
import codecs

class Data_FincaRaiz:
    def __init__(self):
        self.time_to_sleep  = 5

    def get_sitemap():
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
        #print(bs_content.prettify())

        reviews = s.find('urlset',attrs={'class':''}).find_all('loc',attrs={'class':''})
        reviews_list = [links.get_text() for links in reviews]

        #print('reviews_list')
        #print(len(reviews_list))
        
        return(reviews_list)

    def filter_by_words(word,reviews_list):

        if any(word in w for w in reviews_list):
            bogota = [s for s in reviews_list if word in s]
        #print(word)
        #print(len(bogota))
        return (bogota)

#data proyect
    def project_name(s):
        project_name = s.find('div',attrs={'class':'row detailContent'}).find_all('h1',attrs={'style':'margin-bottom: 0px; line-height: 95%;'})
        project_name = [w.get_text() for w in project_name]
        return(project_name)

    def project_zone(s):
        project_zone = s.find('div',attrs={'class':'row detailContent'}).find_all('span',attrs={'class':'font-light'})
        project_zone = [w.get_text() for w in project_zone]
        return(project_zone)

    def project_addres(s):
        project_addres = s.find('div',attrs={'class':'row detailContent'}).find_all('span',attrs={'class':'address'})
        project_addres = [w.get_text() for w in project_addres]
        return(project_addres)  

    def project_owner(s):
        project_owner = s.find('div',attrs={'class':'contact-form'}).find('div',attrs={'class':'tCenter'}).find_all('a',attrs={'class':''})
        project_owner = [w.get_text() for w in project_owner]
        project_owner = project_owner[1]
        return(project_owner)    

    def project_estrato(s):
        project_estrato = s.find('div',attrs={'class':'row features_2 '}).find('ul',attrs={'class':'boxcube'}).find_all('li',attrs={'class':''})
        project_estrato = [w.get_text() for w in project_estrato]
        a=project_estrato[2]
        project_estrato=[int(s) for s in a.split() if s.isdigit()]
        return(project_estrato)



########################################################
    def compute(self):           
        sitetmap = Data_FincaRaiz.get_sitemap()
        print(sitetmap)
        bogota = Data_FincaRaiz.filter_by_words("bogota",sitetmap)
        bogota_proyecto_nuevo = Data_FincaRaiz.filter_by_words("proyecto-nuevo",bogota)
        #return(len(bogota_proyecto_nuevo))
        
        print(len(bogota_proyecto_nuevo))

        j = 420

        while j <= (len(bogota_proyecto_nuevo)-1):


        #for links in bogota_proyecto_nuevo:
            print(j)

            response = requests.get(bogota_proyecto_nuevo[j])
            s = BeautifulSoup(response.text, 'lxml')
            print(Data_FincaRaiz.project_name(s))
            print(Data_FincaRaiz.project_zone(s))
            print(Data_FincaRaiz.project_addres(s))
            print(Data_FincaRaiz.project_owner(s))
            #print(Data_FincaRaiz.project_estrato(s))
        
            j=j+1

        return(True)
    