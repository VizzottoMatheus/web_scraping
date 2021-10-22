import pandas as pd
import datetime
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import cidades_scrape
from funcoes_scrape import encontra_caixa
from funcoes_scrape import proxima_pagina
from funcoes_scrape import extrai_elementos

cidades = cidades_scrape.cidades      # CIDADES QUE O SCRAPER IRÁ BUSCAR
dia = datetime.datetime.today()       # DIA DE HOJE
dia = datetime.datetime.strftime(dia, format = "%d-%m-%Y")

###########################################
######           NAVEGADOR           ######
###########################################

path = # chromedriver path
driver = webdriver.Chrome(executable_path=path)

url = "https://www.trivago.com.br/?aDateRange%5Barr%5D=2021-09-09&aDateRange%5Bdep%5D=2021-09-10&aPriceRange%5Bfrom%5D=0&aPriceRange%5Bto%5D=0&iRoomType=7&aRooms%5B0%5D%5Badults%5D=2&cpt2=59444%2F200&hasList=1&hasMap=1&bIsSeoPage=0&sortingId=1&slideoutsPageItemId=&iGeoDistanceLimit=20000&address=&addressGeoCode=&offset=0&ra=&overlayMode="
driver.get(url)

###########################################
#####   BARRA DE PESQUISA TRIVAGO    ######
###########################################

procurar = '/html/body/div[2]/div[2]/div[3]/div/div[1]/div[2]/form/div/div[1]/div/input'    # BARRA (CAIXA)
pesquisar = '/html/body/div[2]/div[2]/div[3]/div/div[1]/div[2]/form/div/button[2]'          # PESQUISAR (BOTÃO)

###########################################
######            SCRAPER            ######
###########################################

preços = []
preços_ = []
lista = range(1, 51)  # NÚMERO DE ITERAÇÕES POR PÁGINA


for cidade in cidades.keys():

    element = driver.find_element_by_xpath(procurar)  # BARRA DE PESQUISA PARA MUNICÍPIO
    element.click()
    element.clear()
    element.send_keys(cidade)
    time.sleep(2)
    element.send_keys(Keys.RETURN)
    time.sleep(5)

    for click in lista:

        for cod in lista:
            try:
                items_caixa = encontra_caixa(cod, driver)   # ENCONTRA A CAIXA DE CADA ESTABELECIMENTO
                cod_ibge = cidades[cidade]                  # PROCURA O CÓDIGO IBGE DO MUNICÍPIO NO DICIONÁRIO "cidades"
                if items_caixa is None:                     # CONTINUAR FOR LOOP QUANDO "items_caixa" RETORNA VAZIO
                    continue
                else:
                    preços.append([cidade, cod_ibge, dia, items_caixa])      # ADICIONA LINHA DO ESTABELECIMENTO À LISTA "preços"
            except Exception as e:
                print(e)
            continue

        try:
            seta = proxima_pagina(click)                                # SELECIONA ELEMENTO PARA PASSAR DE PÁGINA
            element = driver.find_element_by_xpath(seta)                # ENCONTRA ELEMENTO DA SETA
        except:
            break
        element.click()                                                 # CLICA PARA MUDAR DE PÁGINA
        time.sleep(5)

    preços_.append(preços)
driver.close()

df = pd.DataFrame(preços_[0], columns=['Município', 'CODIGBE', 'Data', 'Itens'])

###################################################
#####        TRATA COLUNA DE LISTAS           #####
###################################################

df_info = extrai_elementos(df, "Itens")
df_final = pd.concat([df[['Município', 'CODIGBE', 'Data']], df_info], axis = 1)
