import re
import pandas as pd

############# FUNÇÃO PARA ENCONTRAR O ELEMENTO QUE PASSA DE PÁGINA ###############
def proxima_pagina(numero):
    seta_pg1 = '/html/body/div[2]/main/div[1]/div[1]/div[3]/div/div[1]/div[2]/div[1]/div/section/nav/div/button/span[1]' # OPÇÃO 1
    seta_pg99 = '/html/body/div[2]/main/div[1]/div[1]/div[3]/div/div[1]/div[2]/div[1]/div/section/nav/div/button[2]/span[1]' # OPÇÃO 2
    if numero == 1:
        pp = seta_pg1
    else:
        pp = seta_pg99
    return pp


####### FUNÇÃO PARA ENCONTRAR O ELEMENTO CORRESPONDENTE A CADA ESTABELECIMENTO ####
def encontra_caixa(numero, driver_):
    xpath01 = f"/html/body/div[3]/main/div[1]/div[1]/div[3]/div/div[1]/div[2]/div[1]/div/section/ol/li[{numero}]/div/article/div[1]/div[2]" # OPÇÃO 1
    xpath02 = f"/html/body/div[2]/main/div[1]/div[1]/div[3]/div/div[1]/div[2]/div[1]/div/section/ol/li[{numero}]/div/article/div[1]/div[2]" # OPÇÃO 2
    xpath03 = f"/html/body/div[2]/main/div[1]/div[1]/div[3]/div/div[1]/div[2]/div[1]/div/section/ol/li[{numero}]/div/li/div/article/div[1]/div[2]" # OPÇÃO 3
    xpaths = [xpath01, xpath02, xpath03]
    for xpath in xpaths:
        try:
            caixa_elem = driver_.find_element_by_xpath(xpath)
            caixa_str = caixa_elem.text
            caixa_items = caixa_str.split("\n")
            caixa_items = [x for x in caixa_items if x is not None]
            return caixa_items
        except Exception as e:
            #print(numero, e)
            continue

######### FUNÇÃO PARA EXTRAIR DADOS DA COLUNA DE LISTAS GERADA DEPOIS DAS EXTRAÇÕES ####
def extrai_elementos(data, coluna_listas):
    """
    DADOS:
    - NOME DO ESTABELECIMENTO
    - TIPO (HOTEL, POUSADA, ETC.)
    - AVALIAÇÕES
    - CAFÉ DA MANHÃ (1 = SIM)
    - PREÇO DA DIÁRIA
    """
    # PADRÕES DOS DADOS A ENCONTRAR NA LISTA
    padrao_nota = re.compile("[0-9]\\.[0-9]$")
    padrao_avaliacoes = re.compile("avalia", flags = re.IGNORECASE)
    padrao_cafe = re.compile("da manh", flags = re.IGNORECASE)
    padrao_preco = re.compile("R\\$", flags = re.IGNORECASE)

    # EXTRAÇÃO DOS DADOS
    l = []
    for estab in data[coluna_listas]:
        new_line = {}
        for num, linha in enumerate(estab):
            if num == 0:                                    # NOME É O PRIMEIRO ELEMENTO DA LISTA
                new_line.update({"Nome": linha})
            if num == 1:                                    # TIPO DE ESTABELECIMENTO É O SEGUNDO ELEMENTO DA LISTA
                new_line.update({"Tipo": linha})
            if re.search(padrao_nota, str(linha)):          # NOTA
                new_line.update({"Nota": linha})
            if re.search(padrao_avaliacoes, str(linha)):    # AVALIAÇÕES
                new_line.update({"Avaliacoes": linha})
            if re.search(padrao_cafe, str(linha)):          # TEM CAFÉ DA MANHÃ?
                new_line.update({"Café": 1})
            if re.search(padrao_preco, str(linha)):         # PREÇO
                new_line.update({"Preço": linha[2:]})
        l.append(new_line)
    return pd.DataFrame(l)