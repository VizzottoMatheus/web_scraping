

#####  ESTÁ FUNCIONANDO!  #####

import tkinter
import os
from urllib.request import urlopen
import urllib.request
from bs4 import BeautifulSoup
import re


url = "http://www.anp.gov.br/dados-abertos-anp/vendas-derivados-petroleo-biocombustiveis"



###############################################################
########################### DADOS #############################
###############################################################
#                                                             #
#  Vendas Gasolina C por segmento (metros cúbicos) 2020       #
#  Vendas Oleo Diesel por segmento (metros cúbicos) 2020      #
#  Vendas Etanol Hidratado por segmento (metros cúbicos) 2020 #
#                                                             #
###############################################################
###############################################################


try:
    html = urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')
    a_nodes = soup.find_all('a', href=True)

    etanol_pattern = re.compile(".*etanol.*hidratado.*segmento.*m3.*2012-2019.csv")
    etanol_2020_pattern = re.compile(".*etanol.*hidratado.*segmento.*m3.*2020.csv")
    gasolinac_pattern = re.compile(".*gasolinac.*segmento.*m3.*2012-2019.csv")
    gasolinac_2020_pattern = re.compile(".*gasolinac.*segmento.*m3.*2020.csv")
    diesel_pattern = re.compile(".*diesel.*segmento.*m3.*2012-2019.csv")
    diesel_2020_pattern = re.compile(".*diesel.*segmento.*m3.*2020.csv")


    links_download = []
    for x in a_nodes:
        if re.search(etanol_pattern, str(x)) or re.search(etanol_2020_pattern, str(x)) or re.search(gasolinac_pattern, str(x)) or \
                re.search(gasolinac_2020_pattern, str(x)) or re.search(diesel_pattern, str(x)) or re.search(diesel_2020_pattern, str(x)):
            links_download.append("http://www.anp.gov.br" + x['href'])

    for x in links_download:
        urllib.request.urlretrieve(x, "{x[48:]}")

    ok = "Download de anp_combustiveis.py efetivado."

except Exception as e:
    print(e)
    erro = f"Problema com anp_combustiveis.py! Processo interrompido.\n({e})"


#############  WINDOW   ###########


root = tkinter.Tk()
canvas1 = tkinter.Canvas(root, width = 300, height = 100)
canvas1.pack()
if ok:
    myLabel = tkinter.Label(root, text = f"{ok}")
else:
    myLabel = tkinter.Label(root, text = f"{erro}")
canvas1.create_window(150, 50, window=myLabel)
root.mainloop()




