#!/usr/bin/env python
# coding: utf-8




import requests
import plotly 
import plotly.express as px
import plotly.io as pio
from bs4 import BeautifulSoup
import pandas as pd
import re
import plotly.graph_objects as go





def plotar_notas_de_corte():
    # Firstly we will get the URL to the site with grades of the second last year
    url = 'https://www.mundovestibular.com.br/enem/sisu/notas-de-corte-sisu-2019/'
    pagina = requests.get(url)

    soup = BeautifulSoup(pagina.content, 'html.parser')
    # Now we will identify all the lines of the web page
    info = soup.find_all('li')
    # Through trial and error we find the lines we want 
    linha = info[22].get_text() 
    # Here follows a function that will organize the text the way we desire
    def prep_linha_v1(linha):
        linha = re.sub('–', "\t", linha)
        return linha

    texto_final = "Curso\tPontos\n"
    #  Next we should apply the function in all the lines we extracted through the use of a for loop
    for i in range(13, 44):
        linha = prep_linha_v1(info[i].get_text())
        texto_final += linha
        if (i < 44):
            texto_final += "\n"
    # For now we will make a file in order to open it in a dataframe
    arquivo = open("lista-cursos.tsv", "w")
    arquivo.write(texto_final)
    arquivo.close()
    df = pd.read_csv("lista-cursos.tsv", sep = '\t', encoding = "latin1")

    # Since the grades we extracted aren't in an average format we will perform operations with the data to gather the average grades
    lst_pontos = list(df['Pontos'])
    lista_pronta = []
    for elements in lst_pontos:
        split = elements.split(' ')
        if len(split) == 5:
            the_number = (float(split[1]) + float(split[3])) / 2
    # This else is necessary in order to maintain some of the grades were extracted already in their average
        else:
            the_number = split[1]

        lista_pronta.append(the_number)

    df['pontos_media'] = lista_pronta
    # Now we will repeat these steps in the website with the grades from last year
    url = 'https://www.guiadacarreira.com.br/educacao/notas-de-corte-enem-2021/'
    pagina = requests.get(url)
    soup = BeautifulSoup(pagina.content, 'html.parser')
    lines = soup.find_all('li')

    def prep_linha_v1(linha):
        linha = re.sub(':', "\t", linha)
        return linha

    texto_final = "Curso\tPontos\n"

    for i in range(55, 74):
        linha = prep_linha_v1(lines[i].get_text())
        texto_final += linha
        if (i < 74):
            texto_final += "\n"


    arquivo = open("lista-cursos-2021.tsv", "w")
    arquivo.write(texto_final)
    arquivo.close()



    df2 = pd.read_csv("lista-cursos-2021.tsv", sep = '\t', encoding = "latin1")

    lst_pontos = list(df2['Pontos'])
    lista_pronta = []
    for elements in lst_pontos:
        split = elements.split(' ')
        if len(split) == 5:
            the_number = (float(split[1]) + float(split[3])) / 2

        else:
            the_number = split[1]

        lista_pronta.append(the_number)
    
    df2['pontos_media'] = lista_pronta
    
    # From now on we will start ornganizing the data in order to plot it in a graph
        # The first step will be to find the common courses bertween the two sites
    cursos_2019 = list(df['Curso'])
    cursos_2020 = list(df2['Curso'])
    cursos_2019_ajuste = []
    for txt in cursos_2019:
        txt = re.sub(' $', "", txt)
        cursos_2019_ajuste.append(txt)
    
    cursos_em_comum = list(set(cursos_2019_ajuste).intersection(cursos_2020))
    # Now that we have a list courses in common we can use it to find the respective grades average from each course 
    
    pontos_2020 = []
    pontos_2019 = []
    for curso in cursos_em_comum:
        temp_df = df.loc[df['Curso'] == curso+' ']
        pontos_2019.append(list(temp_df['pontos_media'])[0])
        temp_df2 = df2.loc[df2['Curso'] == curso]
        pontos_2020.append(list(temp_df2['pontos_media'])[0])

    # After extracting the courses in common and its respecive grades all that is left is to plot the graph
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=cursos_em_comum,
        y=pontos_2019,
        name='Nota 2019',
        marker_color='indianred'
    ))
    fig.add_trace(go.Bar(
        x=cursos_em_comum,
        y=pontos_2020,
        name='Nota 2020',
        marker_color='lightsalmon'
    ))

    # We tilt the angle of the x text in order to be more visible
    fig.update_layout(barmode='group', xaxis_tickangle=-45)
    fig.show()
plotar_notas_de_corte()







