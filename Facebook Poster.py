#!/usr/bin/env python
# -*- coding: utf-8 -*-
#python 3.6

from facepy import GraphAPI
import random
from datetime import datetime
import urllib2

#seu token
access_tokenMe = 'EXDECEdEose0cBAG69XnnVj5Qd91Xeha4q6ebfTQnECyj12oGvAi5DWFkViP6ERlsttMNs0W0dRxBnG1bMrtPzpXk1e22VGFYGnuHZC3MAsNGLqJhSat7njBnIx01ahkfp8a0Res3hyn5QvZB78Yi8x5MjJlbdFWcZAGJEAO6fgjkQE2GeZAnBBs2nUBeaaOgZD'

#atualizar o token quando for usar
access_token = 'EXDCEdEose0cBADBMvVJXMx3AuSFeLtGcrLOsaBxJycK0efWZB1O2UtvGu4leH0ijPtLjD7HLgLcpwGHWDODNZCqWZAZBVLedFV4WFheVTXwyXtVSEcUAi5HTUFRyYGXDlAdJmNWWbiMbPQNOnoghB4P7L6ljZC3P9XYtLeM0EIGTD66ok09u8aHFl5jGi2uAZD'
graph = GraphAPI(access_token)
pageID = '4714525932142025'

# Get my latest posts
#graph = graph.get('me/posts')
#print graph


#Abrir arquivo xml com as ofertas
arquivo = open('LomadeeDownload.xml', 'r')
arquivoLines = arquivo.readlines()
arquivo.close()

#tratar dados do URL
for line in arquivoLines:
    search = "<offer>"
    if search in line:
        produtos = open('Products.txt', 'w')
        for x in range(15):
            line2 = line.split('</offer>')[x]
            produtos.write(line2 + '\n')

produtos.close()

produtosNomes = []
produtosPrecos = []
produtosLink = []
produtosPhotos = []
produtosDescontos = []

produtosNew = open('Products.txt','r')
produtosLines = produtosNew.readlines()
for line1 in produtosLines:
    if '<offerName>' in line1:
        pNome = line1.split('<offerName>')[1].split('</offerName>')[0]
        produtosNomes.append(pNome)
    if '<offerThumbnail>' in line1:
        pPhoto = line1.split('<offerThumbnail>')[1].split('</offerThumbnail>')[0]
        produtosPhotos.append(pPhoto)
    if '<discountPercentage>' in line1:
        pPorcentagem = line1.split('<discountPercentage>')[1].split('</discountPercentage>')[0]
        produtosDescontos.append(pPorcentagem + '%')
    if '<offerLink>' in line1:
        pLink = line1.split('<offerLink>')[1].split('</offerLink>')[0]
        produtosLink.append(pLink)
    if '<priceTo>' in line1:
        pPrice = line1.split('<priceTo>')[1].split('</priceTo>')[0]
        produtosPrecos.append('R$ ' + pPrice)

produtosNew.close()


timestampHours = []

def horaAtual():
    #Descobrir a hora atual em timestamp
    oneHour = 3600
    oneMin = 60
    oneDay = 86400
    
    now = datetime.now()
    #print now
    link = 'http://www.unixtimestamp.com/index.php'
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'}
    req = urllib2.Request(link, headers=hdr)
    page = urllib2.urlopen(req)
    
    text1 = '<h3 class="text-danger">1'
    content2 = page.read()
    if text1 in content2:
        timestampNow0 = content2.split('<h3 class="text-danger">')[1].split('<small>')[0]
        dayNum = input('Quantos dias a frente voce que postar ? ')
        timestampNow = int(timestampNow0) + (dayNum * oneDay)
        timestampHours.append(int(timestampNow) + (11*oneMin))

    for x in range(len(produtosNomes)):
        timestampNow = int(timestampNow) + oneHour
        timestampHours.append(int(timestampNow))

    



#Abrir arquivos de mensagen Text
arquivo1 = open('messagesText.txt', 'r')
arquivoLines1 = arquivo1.readlines()
messageText = []
for line1 in arquivoLines1:
    line1 = line1.split('\n')[0]
    messageText.append(line1)
    
arquivo1.close()


path1 = 'me/photos'



#Analisar e fazer backup de posts repetidos
postsList = []
arquivo2 = open('Posts.txt','r')
arquivoLines2 = arquivo2.readlines()

for line2 in arquivoLines2:
    line2 = line2.split('\n')[0]
    postsList.append(line2)

arquivo2.close()






def postMsg():
    # Post a photo and a message
    #graph.post(message = message1,path = path1,link = link1,source = source1)
    maxNum = len(produtosNomes)
    for x in range(maxNum):
        if produtosNomes[x] in postsList:
            print 'Repetido'
        else:
            fileMsg = produtosNomes[x] + '\n' + 'Com ' + produtosDescontos[x] + ' de desconto.\n'  + 'Por apenas: ' + produtosPrecos[x] + '\n' + 'Acesse: ' + produtosLink[x]
            message1 = fileMsg +  '\n Acesse : http://www.viajebastante.esy.es/'
            path1 = 'me/photos'
            link1 = 'http://www.viajebastante.esy.es/'
            source1 = produtosLink[x]
            # Post a photo and a message scheduled
            graph.post(message = fileMsg ,path = 'me/feed', link = source1 ,scheduled_publish_time =int(timestampHours[x]), published = 'false')

            postsList.append(produtosNomes[x])
            print ('Post ' + str(x) + ' - Done!' )

def backupPosts():
    arquivo3 = open('Posts.txt','w')
    for x in produtosNomes:
            arquivo3.write(x + '\n')

    arquivo3.close()


#Call the functions
horaAtual()
postMsg()
backupPosts()
