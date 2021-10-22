

#####  ESTÁ FUNCIONANDO!  #####

import re
import os
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import pandas as pd
import tkinter
from selenium.webdriver.support.ui import WebDriverWait


path = # chromedriver path


###############################  BAIXA ARQUIVOS  ##############################



ANP_pattern = re.compile("ANP.*.xls")

try:
    driver = webdriver.Chrome(executable_path=path)
    driver.get('https://postos.anp.gov.br/consulta.asp')

    def every_downloads_chrome(driver):
        if not driver.current_url.startswith("chrome://downloads"):
            #driver.execute_script("window.open('');")
            #driver.switch_to.window(driver.window_handles[1])
            driver.get("chrome://downloads/")
        return driver.execute_script("""
            var elements = document
            .querySelector('downloads-manager')
            .shadowRoot.querySelector('#downloadsList').items;
            if (elements.every(e => e.state === "COMPLETE"))
                   return elements.map(elements =>elements.fileUrl || elements.file_url);
            """)


    sigla = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS" , "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]

    def download():
        for x in sigla:
            select = Select(driver.find_element_by_name("sEstado"))
            select.select_by_visible_text(f'{x}')
            pesquisa = driver.find_element_by_name('bPesquisar')
            pesquisa.click()
            extrai = driver.find_element_by_name('Submit1')
            extrai.click()
            #time.sleep(2)

            paths = WebDriverWait(driver, 120, 1).until(every_downloads_chrome)
            driver.get('https://postos.anp.gov.br/consulta.asp')

    download()
    driver.quit()
    ok = "Download de anp_postos.py efetivado."


except Exception as e:
    exception = e
    driver.quit()
    erro = "Problema com download de anp_postos.py! Processo interrompido."

###############################      AJUSTE TABELA    #################################

#### uso read_html porque não é um arquivo xls (pd.read_excel gera erro)  ####


padrao_estado = re.compile("[A-Z][A-Z].xls$")
try:
    d = {}
    for x in os.listdir("C:\\Users\\matheus.vizzotto\\Desktop\\Banco_Dados\\ANP\\Scrape"):
        if re.search(padrao_estado,x):
            ####  ADICONEI HEADER = 0 POIS ESTAVA RECONHECENDO OS NOMES DA COLUNA COMO NÚMEROS  #####
            ### PARA MUDAR COLUNA ÍNDICE, index_col = x DENTRO DE pd.read  ###

            d["{0}".format(x[:-4])] = pd.DataFrame(pd.read_html(f"{x}", header=0)[1])

    df = pd.DataFrame(d["AC"])

    del d["AC"]

    for x in d:
        df = pd.concat([df, d[x]], axis=0)

    if "AGREGADO.xlsx" in os.listdir("C:\\Users\\matheus.vizzotto\\Desktop\\Banco_Dados\\ANP\\Scrape"):
        os.remove("C:\\Users\\matheus.vizzotto\\Desktop\\Banco_Dados\\ANP\\Scrape\\AGREGADO.xlsx")
        df.to_excel("C:\\Users\\matheus.vizzotto\\Desktop\\Banco_Dados\\ANP\\Scrape\\AGREGADO.xlsx")
    else:
        df.to_excel("C:\\Users\\matheus.vizzotto\\Desktop\\Banco_Dados\\ANP\\Scrape\\AGREGADO.xlsx")

    ok2 = "Tabela de anp_postos.py agregada."
except Exception as e:
    exception2 = e
    print(exception2)
    erro2 = "Problema com agregação da tabela de anp_postos! Processo interrompido."


########################################################################################################


sigla_estado = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS" , "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]
postos_interesse = ["BANDEIRA BRANCA", "IPIRANGA", "CHARRUA", "RAIZEN", "ALESAT", "RODOIL", "MAXSUL", "STANG", "PETROBRAS DISTRIBUIDORA S.A.", "SUL COMBUSTÍVEIS", "POTENCIAL", "CIAPETRO", "AMERICANOIL", "DIBRAPE", "WALENDOWSKY", "RAIZEN MIME"]


d = []
for x in postos_interesse:
    tabela_filtrada_empresa = tabela[tabela['Vinculação a Distribuidor'] == x]
    postos_br = tabela_filtrada_empresa['CNPJ'].nunique()
    new_row = {"Empresa": '{}'.format(x), "Postos no Brasil": postos_br}
    for estado in sigla_estado:
        tabela_filtrada_estado = tabela_filtrada_empresa[tabela_filtrada_empresa['UF'] == estado]
        postos_estado = tabela_filtrada_estado['CNPJ'].nunique()
        new_row.update({"{}".format(estado): postos_estado})
    d.append(new_row)

df = pd.DataFrame(d)
df.to_excel("Num_Postos.xlsx")


##############  WINDOW  #################
try:
    ok
except NameError:
    ok = None
try:
    ok2
except NameError:
    ok2 = None
try:
    erro
except NameError:
    erro = None
try:
    erro2
except NameError:
    erro2 = None
try:
    exception
except NameError:
    exception = None
try:
    exception2
except NameError:
    exception2 = None


root = tkinter.Tk()
canvas1 = tkinter.Canvas(root, width = 300, height = 100)
canvas1.pack()
if ok and ok2:
    myLabel = tkinter.Label(root, text = f"{ok}\n{ok2}")
else:
    if erro and erro2:
        myLabel = tkinter.Label(root, text = f"{erro}\n({exception}\n\n{erro2}\n{exception2})")
    if erro and erro2 == None:
        myLabel = tkinter.Label(root, text=f"{erro}\n({exception})")
    if erro2 and erro == None:
        myLabel = tkinter.Label(root, text=f"{erro2}\n{exception2})")
canvas1.create_window(150, 50, window=myLabel)
root.mainloop()
