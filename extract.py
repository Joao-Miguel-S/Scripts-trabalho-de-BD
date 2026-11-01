import csv
import json

senador_viagem = []

with open('CSV/Viagens.csv', 'r', encoding='UTF-8') as arquivo:
    leitor = csv.reader(arquivo, delimiter=',', quotechar='"')
    for linha in leitor:
        
        compraAerea = {
            "motivo": linha[0],
            "resumoDoMotivo": linha[1],
            "passageiro": linha[3],
            "statusPassageiro": linha[4],
            "dataIda":linha[10],
            "dataVolta":linha[11],
            "tarifa":linha[13] ,
            "valorReembolso":linha[29],
            "taxasExtras:": linha[27]
        }

        seguro = {
            "regiao":linha[9],
            "bilhete":linha[6],
            "seguradora":linha[7]
        }

        passagem = {
            "trechos":linha[9],
            "ciaAerea":linha[7],
            "voucher":linha[6],
            "taxaEmbarque":linha[15],
            "classe":linha[24]
        }

        combined ={}

        if(linha[5]=="Seguro Viagem"):
            combined = {**compraAerea,**seguro}
        else:
            combined = {**compraAerea,**passagem}


        senador_viagem.append(combined)



with open('JSON/Viagens.json','w',encoding='utf-8') as fJSON:
        json.dump(senador_viagem,fJSON,ensure_ascii=False,indent=4)


with open('CSV/Viagens.csv', 'r', encoding='UTF-8') as arquivo:
    leitor = csv.reader(arquivo, delimiter=',', quotechar='"')
    for linha in leitor:
        
        compraAerea = {
            "motivo": linha[0],
            "resumoDoMotivo": linha[1],
            "passageiro": linha[3],
            "statusPassageiro": linha[4],
            "dataIda":linha[10],
            "dataVolta":linha[11],
            "tarifa":linha[13] ,
            "valorReembolso":linha[29],
            "taxasExtras:": linha[27]
        }

        seguro = {
            "regiao":linha[9],
            "bilhete":linha[6],
            "seguradora":linha[7]
        }

        passagem = {
            "trechos":linha[9],
            "ciaAerea":linha[7],
            "voucher":linha[6],
            "taxaEmbarque":linha[15],
            "classe":linha[24]
        }

        combined ={}

        if(linha[5]=="Seguro Viagem"):
            combined = {**compraAerea,**seguro}
        else:
            combined = {**compraAerea,**passagem}


        senador_viagem.append(combined)



