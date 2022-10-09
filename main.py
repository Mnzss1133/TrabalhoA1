import pandas as pd
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import seaborn as sns
##Scapping da Wikipedia
url='https://pt.wikipedia.org/wiki/Discografia_de_Justin_Bieber'
ouvirmusica = requests.get(url)
conteudo = ouvirmusica.content
site= BeautifulSoup(conteudo, 'html.parser')
#Scrapping do album Journals, que não era possível pegar ele através do link da wikipedia normal
url3 = 'https://pt.wikipedia.org/wiki/Journals'
Journals = requests.get(url3)
content3= Journals.content
site3 = BeautifulSoup(content3, 'html.parser')
lista_duracao=[]
lista_Journals = []

tabela = site3.find('div', attrs={'style': 'padding:4px'})

for nome in tabela.find_all('td', attrs={'style': 'text-align: left; vertical-align: top;'}):
    lista_Journals.append(nome.text)

lista_Journals = [item.replace("\xa0", "") for item in lista_Journals]
lista_Journals = [item.replace("\n", "") for item in lista_Journals]
lista_Journals = [item.replace('" ', '') for item in lista_Journals]
lista_Journals = [item.replace('"', '') for item in lista_Journals]
lista_Journals.remove('Flatline (no iTunes por tempo limitado)')
lista_Journals.remove('Alone (no iTunes por tempo limitado)')

for duracao in site3.find_all('td', attrs={'style': 'padding-right: 10px; text-align: right; vertical-align: top;'}):
    lista_duracao.append(duracao.get_text())
for nome in lista_duracao:
    if (nome == '1.','2.'):
            lista_duracao.remove(nome)
lista_duracao.remove('2:20')
lista_duracao.remove('3:39')



#Foi preciso pegar o album justice de uma outra página dentro da wikipedia, pois no primeira página a minutagem não aparecia.
url2 = 'https://en.wikipedia.org/wiki/Justice_(Justin_Bieber_album)'
Justice = requests.get(url2)
content2 = Justice.content
site2 = BeautifulSoup(content2, 'html.parser')
lista_duracao2=[]

for musica in site2.find_all('td', attrs={'class': 'tracklist-length'}):
    lista_duracao2.append(musica.get_text())
#Dentro do site das letras o comando entrará em cada uma das músicas e obterá a sua letra e colocará em uma lista
site2_musicas = site.find('table', attrs={'class':'wikitable'})
lista_musica = []
lista_Duracao = []
for links in site2_musicas.findAll('a'):
    link_musica = 'https://pt.wikipedia.org' + links['href']
    request_ouvirmusica = requests.get(link_musica)
    conteudo_letra = request_ouvirmusica.content
    site_musica = BeautifulSoup(conteudo_letra, 'html.parser')
    for musica in site_musica.find_all('td', attrs={'style': 'text-align: left; vertical-align: top;'}):
        lista_musica.append(musica.get_text())
    for duracao in site_musica.find_all('td', attrs={'style': 'padding-right: 10px; text-align: right; vertical-align: top;'}):
        lista_Duracao.append(duracao.get_text())

lista_musica = [item.replace("\xa0", "") for item in lista_musica]
lista_musica = [item.replace('"', "") for item in lista_musica]
lista_Duracao = [item.replace("\xa0", "") for item in lista_Duracao]
for nome in lista_Duracao:
    if (nome == '1.','2.'):
        lista_Duracao.remove(nome)

#Album My World

album_MyWorld = lista_musica[0:10]
album_MyWorld_duracao = lista_Duracao[0:10]
My_World_df = pd.DataFrame(zip(album_MyWorld,album_MyWorld_duracao),
                     columns=['Música','Duração'])
My_World_df ['Duração']=My_World_df ['Duração'].str.replace(':','.').astype(float)

#UnderTheMistletoe
album_Under_The_Mistletoe = lista_musica[10:21]
album_Under_The_Mistletoe_Duracao = lista_Duracao[10:21]
Under_The_Mistletoe_df =pd.DataFrame(zip(album_Under_The_Mistletoe,album_Under_The_Mistletoe_Duracao),
                                     columns=['Música','Duração'])
Under_The_Mistletoe_df['Duração']=Under_The_Mistletoe_df['Duração'].str.replace(':','.').astype(float)

# Album Believe
album_believe = lista_musica[25:38]
album_believe_Duracao = lista_Duracao[25:38]

believe_df = pd.DataFrame(zip(album_believe,album_believe_Duracao),
                          columns=['Música', 'Duração'])
believe_df['Duração']=believe_df['Duração'].str.replace(':','.').astype(float)
#Album Journals

album_Journals = lista_Journals
album_Journals_Duração = lista_duracao
Journals_df = pd.DataFrame(zip(album_Journals,album_Journals_Duração),
                          columns=['Música', 'Duração'])
Journals_df['Duração']=Journals_df['Duração'].str.replace(':','.').astype(float)


#Album Purpose
album_Purpose = lista_musica[44:57]
album_Purpose_Duracao = lista_Duracao[44:57]
Purpose_df = pd.DataFrame(zip(album_Purpose,album_Purpose_Duracao),
                          columns=['Música','Duração'])

Purpose_df['Duração']=Purpose_df['Duração'].str.replace(':','.').astype(float)
Purpose_df.to_csv("Purpose_df")

#Album Changes
album_Changes = lista_musica[68:84]
album_Changes_Duracao = lista_Duracao[68:84]

Changes_df = pd.DataFrame(zip(album_Changes,album_Changes_Duracao),
                          columns=['Música','Duração'])
Changes_df['Duração']=Changes_df['Duração'].str.replace(':','.').astype(float)
Changes_df.to_csv("Changes_df.csv")

#Album Justice
album_Justice=lista_musica[87:103]
album_Justice_Duracao = lista_duracao2[0:16]
Justice_df =pd.DataFrame(zip(album_Justice,album_Justice_Duracao),
                         columns=['Música','Duração'])
Justice_df['Duração']=Justice_df['Duração'].str.replace(':','.').astype(float)

Justice_df.to_csv('Justice_df')


album_musicas = album_MyWorld+album_Under_The_Mistletoe+album_believe+album_Journals+album_Purpose+album_Changes+album_Justice
album_Duração = album_MyWorld_duracao+album_Under_The_Mistletoe_Duracao+album_believe_Duracao+album_Journals_Duração+album_Purpose_Duracao+album_Changes_Duracao+album_Justice_Duracao

dados={"Música":album_musicas,"Duração":album_Duração}
DF_principal = pd.DataFrame(data=dados)
DF_principal['Duração']=DF_principal['Duração'].str.replace(':','.').astype(float)


#Respondendo as questões
#Grupo 1

def musica_mais_longa_My_My_World():
    maior_tempo_MyWorld =  My_World_df[['Música', 'Duração']].nlargest(n=3, columns='Duração', keep='first')
    return f'As músicas mais longa do album My World são  : \n {maior_tempo_MyWorld}'
#print(musica_mais_longa_My_My_World())
def musica_mais_curta_My_My_World():
    menor_tempo_MyWorld= My_World_df[['Música', 'Duração']].nsmallest(n=3, columns='Duração', keep='first')
    return f'As músicas mais curtas do album My World são  : \n {menor_tempo_MyWorld}'
#print(musica_mais_curta_My_My_World())
def musica_mais_longa_Under_The_Mistletoe():
    maior_tempo_Under = Under_The_Mistletoe_df[['Música', 'Duração']].nlargest(n=3, columns='Duração', keep='first')
    return f'As músicas mais longa do album under the mistletoe são  : \n {maior_tempo_Under}'
#print(musica_mais_longa_Under_The_Mistletoe())
def musica_mais_curta_Under_The_Mistletoe():
    menor_tempo_Under = Under_The_Mistletoe_df[['Música', 'Duração']].nsmallest(n=3, columns='Duração', keep='first')
    return f'As músicas mais curtas do album under the mistletoe são  : \n {menor_tempo_Under}'
#print(musica_mais_curta_Under_The_Mistletoe())

def musica_mais_longa_album_believe():
    maior_tempo_Believe = believe_df[['Música','Duração']].nlargest(n=3,columns='Duração',keep ='first')
    return f'As músicas mais longas do album believe são  : \n { maior_tempo_Believe}'
#print(musica_mais_longa_album_believe())

def musica_mais_curta_album_believe():
    menor_tempo_Believe = believe_df[['Música','Duração']].nsmallest(n=3,columns='Duração',keep ='first')
    return f'As músicas mais curtas do album believe são  : \n {menor_tempo_Believe}'
#print(musica_mais_curta_album_believe())

def musica_mais_longa_album_Journals():
    menor_tempo_Journals = Journals_df[['Música', 'Duração']].nsmallest(n=3, columns='Duração', keep='first')
    return f'As músicas mais longas do album Journals são  : \n {menor_tempo_Journals}'

#print(musica_mais_longa_album_Journals())

def musica_mais_curta_album_Journals():
    maior_tempo_Journals = Journals_df[['Música','Duração']].nsmallest(n=3,columns='Duração',keep ='first')
    return f'As músicas mais curtas do album Journals são  : \n {maior_tempo_Journals}'

#print(musica_mais_curta_album_Journals())

def musica_mais_longa_album_Purpose():
    maior_tempo_Purpose= Purpose_df[['Música','Duração']].nlargest(n=3,columns='Duração',keep ='first')
    return f'As músicas mais longas do album Purpose são  : \n {maior_tempo_Purpose}'
#print(musica_mais_longa_album_Purpose())

def musica_mais_curta_album_Purpose():
    menor_tempo_Purpose = Purpose_df[['Música','Duração']].nsmallest(n=3,columns='Duração',keep ='first')
    return f'As músicas mais curtas do album Purpose são  : \n {menor_tempo_Purpose}'
#print(musica_mais_curta_album_Purpose())
def musica_mais_longa_album_Changes():
    maior_tempo_changes = Changes_df[['Música','Duração']].nlargest(n=3,columns='Duração',keep ='first')
    return f'As músicas mais longas do album Changes são  : \n { maior_tempo_changes}'

#print(musica_mais_longa_album_Changes())
def musica_mais_curta_album_Changes():
   menor_tempo_changes= Changes_df[['Música','Duração']].nsmallest(n=3,columns='Duração',keep ='first')

   return f'As músicas mais curtas do album Changes são  : \n {menor_tempo_changes}'
#print(musica_mais_curta_album_Changes())

def musica_mais_longa_album_Justice():
    maior_tempo_justice= Justice_df[['Música','Duração']].nlargest(n=3,columns='Duração',keep ='first')
    return f'As músicas mais longas do album Justice são  : \n {maior_tempo_justice}'
#print(musica_mais_longa_album_Justice())

def musica_mais_curta_album_Justice():
    menor_tempo_Justice= Justice_df[['Música','Duração']].nsmallest(n=3,columns='Duração',keep ='first')
    return f'As músicas mais curtas do album Justice são  : \n {menor_tempo_Justice}'
#print(musica_mais_curta_album_Justice())

def musicas_mais_tocada_da_história():
    maior_tempo =DF_principal[['Música', 'Duração']].nlargest(n=3, columns='Duração', keep='first')
    return f'As musicas com maior tempo são :\n {maior_tempo} '
#print(musicas_mais_tocada_da_história())

def musicas_menos_tocada_da_história():
    menor_tempo =DF_principal[['Música', 'Duração']].nsmallest(n=3, columns='Duração', keep='first')
    return f'As musicas com menor tempo são :\n {menor_tempo} '
#print(musicas_menos_tocada_da_história())



# Grupo 3 
def media():
    DF_principal_media = DF_principal['Duração'].mean()
    return f'f A media da duracao de todas as músicas é de {DF_principal_media}'
print(media)



