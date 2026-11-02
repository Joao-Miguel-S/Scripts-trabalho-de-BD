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
    with open('SQL/Senador.sql','w',encoding='utf-8') as f:
        None
    with open('SQL/Contrata.sql','w',encoding='utf-8') as f:
        None
    with open('SQL/AuxilioMoradia.sql','w',encoding='utf-8') as f:
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
        return "NULL"  #retorna uma data padrão para valores nulos ou vazios
    try:
        parts = date_str.split('/')
        if len(parts) == 3:
            return f"'{parts[2]}-{parts[1]}-{parts[0]}'"
    except:
        pass
    return "NULL"

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
        id = 1;
        for item in dadosContratos:
            insert = "INSERT INTO Contrata VALUES ({0},'{1}','{2}','{3}',{4},'{5}','{6}','{7}', {8});\n".format(
                item["senador"]["codSenador"],                  
                item["beneficiario"]["documento"],              
                item["data"],                                   
                item["documento"],                              
                stringToFloat(item["valor"]),                   
                item["tipoDespesa"],                            
                item["detalhamento"],                           
                item["tipoDocumento"],
                id
            )
            f.write(insert)
            id += 1


with open('JSON/Viagens.json',"r", encoding='utf-8') as file:
    comprasAereas = json.load(file)

    for compraAerea in comprasAereas:
        if(compraAerea["tipo"]=="Seguro Viagem"):
            with open('SQL/Seguro.sql','a',encoding='utf-8') as f:
                    try:
                        insert = "INSERT INTO Seguro values ('{0}','{1}','{2}','{3}','{4}','{5}',{6},{7},{8},'{9}','{10}','{11}',{12});\n".format(
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
                    insert = "INSERT INTO Passagem values ('{0}','{1}',{2},'{3}','{4}','{5}','{6}',{7},{8},{9},{10},{11},{12},{13});\n".format(
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
                for i in range(len(compraAerea["trechos"]) - 1):
                    with open('SQL/Trechos.sql','a',encoding='utf-8') as Pass:
                        insert = "INSERT INTO Trechos values ({0},'{1}','{2}','{3}');\n".format(
                            (i + 1),
                            compraAerea["trechos"][0],
                            compraAerea["trechos"][1],
                            compraAerea["voucher"],
                        )
                        Pass.write(insert)
            except:
                continue

with open('JSON/auxilioMoradia.json',"r", encoding='utf-8') as file:
	auxiliosMoradia = json.load(file)

	with open('SQL/AuxilioMoradia.sql','w',encoding='utf-8') as f:
		for auxilioMoradia in auxiliosMoradia:
			insert = "INSERT INTO AuxilioMoradia values ({0}, {1}, {2});\n".format(
				auxilioMoradia["data"],
				auxilioMoradia["recebeu"],
                auxilioMoradia["codSenador"]
		)
			f.write(insert)

with open('JSON/Beneficiario.json',"r", encoding='utf-8') as file:
    beneficiarios = json.load(file)

    with open('SQL/Beneficiario.sql','w',encoding='utf-8') as f:
        for beneficiario in beneficiarios:
            insert = "INSERT INTO Beneficiario values ('{0}', '{1}');\n".format(
                beneficiario["documento"],
                beneficiario["nome"]
        )
            f.write(insert)


with open('JSON/filiacao.json', "r", encoding='utf-8') as file:
    senadorPartidos = json.load(file)

    with open('SQL/SenadorPartido.sql', 'w', encoding='utf-8') as f:
        for item in senadorPartidos:
            data_ingresso = f"'{item['dataFiliacao']}'" if item["dataFiliacao"].strip() else "NULL"
            
            data_saida = f"'{item['dataDesfiliacao']}'" if item["dataDesfiliacao"].strip() else "NULL"

            insert = "INSERT INTO SenadorPartido VALUES ({0}, '{1}', {2}, {3});\n".format(
                item["codSenador"],
                item["nomePartido"].upper(),
                data_ingresso,
                data_saida
            )
            f.write(insert)

with open('JSON/Partidos.json', "r", encoding='utf-8') as file:
    partidos = json.load(file)

    with open('SQL/Partidos.sql', 'w', encoding='utf-8') as f:
        for partido in partidos:
            insert = "INSERT INTO Partidos VALUES ('{0}','{1}','{2}');\n".format(
                partido["nome"],
                partido["sigla"],
                partido["presidente"].title(),
            )
            f.write(insert)

with open('JSON/servidores.json',"r", encoding='utf-8') as file:
    servidores = json.load(file)

    with open('SQL/Servidores.sql','w',encoding='utf-8') as f:
        for servidor in servidores:
            insert = "INSERT INTO Servidor values ({0}, '{1}', {2}, {3}, '{4}', {5});\n".format(
                servidor["id"],
                servidor["cargo"],
                stringToFloat(servidor["remuneracaoBasica"]),
                stringToFloat(servidor["remuneracaoLiquida"]),
                servidor["data"],
                servidor["codSenador"]
        )
            f.write(insert)