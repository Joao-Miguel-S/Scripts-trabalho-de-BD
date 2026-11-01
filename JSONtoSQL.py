import json
import difflib

def resetFiles():
    with open('SQL/Seguro.sql','w',encoding='utf-8') as f:
        None
    with open('SQL/Passagem.sql','w',encoding='utf-8') as f:
        None
    with open('Files/Relatorio.txt','w',encoding='utf-8') as R:
        None
    with open('Files/NaoEncontrados.txt','w',encoding='utf-8') as N:
        None

def betterDictSenador(dict):
    senDict = {}
    for element in dict:
        senDict[element["nome"]] = element["codSenador"]
    return senDict

#Função para transforma os números do json em float
def stringToFloat(value):
    try:
        if(value==""  or value=="-" or value==" "):
            return 0
        else:
            return float(value.replace('.','').replace(',','.'))
    except:
        print(value+" tentou ser transformado\n")
        return 0

#O unico elemento que liga o senador a uma passagem é o seu nome, contudo, pode estar escrito de forma distinta.
#A função a baixo tem o objetivo de encontrar um senador com o nome mais parecido a uma passagem.
def findSenador(senDict,name):
    try:
        senadorArray = []
        for key,value in senDict.items():
            senadorArray.append(key)
        closeNames = difflib.get_close_matches(name,senadorArray,1,0.6)
    
        with open('Files/Relatorio.txt','a',encoding='utf-8') as R:
            R.write(name+" -> "+closeNames[0]+"\n")
        return closeNames[0]
    except:
        with open('Files/NaoEncontrados.txt','a',encoding='utf-8') as N:
            N.write(name+"\n")
        return None

Senadores = {}
comprasAereas = {}
resetFiles()
with open('JSON/Senador.json',"r") as file:
        Senadores = json.load(file)

        with open('SQL/Senador.sql','w',encoding='utf-8') as f:
            for senador in Senadores:
                insert = "INSERT INTO Senador values ({0},'{1}','{2}','{3}','{4}','{5}','{6}');\n".format(senador["codSenador"],senador["nome"], senador["uf"],senador["sexo"],senador["email"],senador["foto"],senador["site"])
                f.write(insert)

senDict = betterDictSenador(Senadores)

with open('JSON/Viagens.json',"r") as file:
        comprasAereas = json.load(file)

        for compraAerea in comprasAereas:
            if(compraAerea["tipo"]=="Seguro Viagem"):
                with open('SQL/Seguro.sql','a',encoding='utf-8') as f:
                        try:
                            insert = "INSERT INTO Seguro values ({0},'{1}','{2}','{3}','{4}',{5},{6},{7},'{8}','{9}','{10}');\n".format(senDict[findSenador(senDict,compraAerea["passageiro"])],compraAerea["motivo"],compraAerea["resumoDoMotivo"],compraAerea["dataIda"],compraAerea["dataVolta"],stringToFloat(compraAerea["tarifa"]),stringToFloat(compraAerea["valorReembolso"]),stringToFloat(compraAerea["taxasExtras"]),compraAerea["regiao"],compraAerea["bilhete"],compraAerea["seguradora"])
                            f.write(insert)
                        except:
                            continue
            else:
                with open('SQL/Passagem.sql','w',encoding='utf-8') as f:
                    insert = "INSERT INTO Senador values ({0},'{1}','{2}','{3}','{4}','{5}','{6}');\n".format(senador["codSenador"],senador["nome"], senador["uf"],senador["sexo"],senador["email"],senador["foto"],senador["site"])
                    f.write(insert)


with open('JSON/Senador.json',"r") as file:
        #create = "CREATE TABLE Senador (codSenador INT, nome VARCHAR(70), uf CHAR(2), sexo VARCHAR(20), email VARCHAR(50),  foto VARCHAR(100), site VARCHAR(100)" \
        #"PRIMARY KEY(codSenador));"
        data = json.load(file)

        with open('SQL/Senador.sql','w',encoding='utf-8') as f:
            for senador in data:
                insert = "INSERT INTO Senador values ({0},'{1}','{2}','{3}','{4}','{5}','{6}');\n".format(senador["codSenador"],senador["nome"], senador["uf"],senador["sexo"],senador["email"],senador["foto"],senador["site"])
                f.write(insert)


