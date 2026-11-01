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

#formata as datas pq tava dando errado no banco
def formatDate(date_str):
    if not date_str or date_str.strip() == "":
        return "0001-01-01"  #retorna uma data padrão para valores nulos ou vazios
    try:
        parts = date_str.split('/')
        if len(parts) == 3:
            return f"{parts[2]}-{parts[1]}-{parts[0]}"
    except:
        pass
    return "0001-01-01"

Senadores = {}
comprasAereas = {}

resetFiles()


with open('JSON/Senador.json',"r", encoding='utf-8') as file:
        Senadores = json.load(file)

        with open('SQL/Senador.sql','w',encoding='utf-8') as f:
            for senador in Senadores:
                insert = "INSERT INTO Senador values ({0},'{1}','{2}','{3}','{4}','{5}','{6}');\n".format(
                    senador["codSenador"],
                    senador["nome"],
                    senador["uf"],
                    senador["sexo"],
                    senador["email"],
                    senador["foto"],
                    senador["site"])
                f.write(insert)

senDict = betterDictSenador(Senadores)

with open('JSON/contrata.json', "r", encoding='utf-8') as file:
    dadosContratos = json.load(file)

    with open('SQL/Contrata.sql', 'w', encoding='utf-8') as f:
        for item in dadosContratos:
            insert = "INSERT INTO Contrata VALUES ({0},'{1}','{2}','{3}',{4},'{5}','{6}','{7}');\n".format(
                item["senador"]["codSenador"],                  
                item["beneficiario"]["documento"],              
                item["data"],                                   
                item["documento"],                              
                stringToFloat(item["valor"]),                   
                item["tipoDespesa"],                            
                item["detalhamento"],                           
                item["tipoDocumento"]                           
            )
            f.write(insert)


with open('JSON/Viagens.json',"r", encoding='utf-8') as file:
        comprasAereas = json.load(file)

        for compraAerea in comprasAereas:
            if(compraAerea["tipo"]=="Seguro Viagem"):
                with open('SQL/Seguro.sql','a',encoding='utf-8') as f:
                        try:
                            insert = "INSERT INTO Seguro values ({0},'{1}','{2}','{3}','{4}','{5}',{6},{7},{8},'{9}','{10}','{11}','{12}');\n".format(
                                compraAerea["regiao"],
                                compraAerea["bilhete"],
                                compraAerea["seguradora"],
                                compraAerea["motivo"],
                                compraAerea["resumoDoMotivo"],
                                compraAerea["tipo"],
                                formatDate(compraAerea["dataIda"]),
                                formatDate(compraAerea["dataVolta"]),
                                stringToFloat(compraAerea["tarifa"]),
                                stringToFloat(compraAerea["valorReembolso"]),
                                stringToFloat(compraAerea["taxasExtras"]),
                                senDict[findSenador(senDict,compraAerea["passageiro"])],
                                formatDate(compraAerea["dataEmissao"])
                            )
                            f.write(insert)
                        except:
                            continue
            else:
                try:
                    with open('SQL/Passagem.sql','a',encoding='utf-8') as Pass:
                        insert = "INSERT INTO Passagem values ('{0}','{1}',{2},'{3}','{4}','{5}','{6}','{7}','{8}',{9},{10},{11},{12},'{13}');\n".format(
                            compraAerea["ciaAerea"],
                            compraAerea["voucher"],
                            stringToFloat(compraAerea["taxaEmbarque"]),
                            compraAerea["classe"],
                            compraAerea["motivo"],
                            compraAerea["resumoDoMotivo"],
                            compraAerea["tipo"],
                            formatDate(compraAerea["dataIda"]),
                            formatDate(compraAerea["dataVolta"]),
                            stringToFloat(compraAerea["tarifa"]),
                            stringToFloat(compraAerea["valorReembolso"]),
                            stringToFloat(compraAerea["taxasExtras"]),
                            senDict[findSenador(senDict,compraAerea["passageiro"])],
                            formatDate(compraAerea["dataEmissao"])
                        )
                        Pass.write(insert)
                except:
                    continue




