#Usando o site ouvirmusica.com.br para conseguir pegas as letras das músicas
url2='https://www.ouvirmusica.com.br/justin-bieber/'
ouvirmusica = requests.get(url2)
conteudo = ouvirmusica.content
site2= BeautifulSoup(conteudo, 'html.parser')

#Dentro do site das letras o comando entrará em cada uma das músicas e obterá a sua letra e colocará em uma lista
site2_musicas = site2.find('ol', attrs={'class':'list'})

lista_letras = []

for links in site2_musicas.findAll('a'):
    link_musica = 'https://www.ouvirmusica.com.br' + links['href']


    request_ouvirmusica = requests.get(link_musica)
    conteudo_letra = request_ouvirmusica.content
    site_letra = BeautifulSoup(conteudo_letra, 'html.parser')

    letras_jb = site_letra.find('div', attrs={'class':'cnt'})
    lista_letras.append(letras_jb.get_text())
#print(lista_letras) 

