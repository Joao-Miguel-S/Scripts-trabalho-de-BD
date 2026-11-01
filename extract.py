import csv
import json

senador_viagem = []
senador_despesas = []
beneficiarioJSON = []
contrataJSON = []


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
            "taxasExtras": linha[27],
            "tipo":linha[5]
        }

        seguro = {
            "regiao":linha[9],
            "bilhete":linha[6],
            "seguradora":linha[7]
        }
        
        trecho = linha[9].split("/")
        
        passagem = {
            "trechos":trecho,
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


with open('CSV/Despesas.csv', 'r', encoding='UTF-8') as arquivo:
    leitor = csv.reader(arquivo, delimiter=';', quotechar='"')
    for linha in leitor:
        beneficiario = {
            "documento":linha[7],
            "nome":linha[8],
        }

        senador_despesa = {
            "codSenador":linha[4],
            "nomeSenador":linha[5],
        }

        contrata = {
            "tipoDocumento":linha[1],
            "documento":linha[9],
            "data":linha[10],
            "valor":linha[12],
            "tipoDespesa":linha[6],
            "senador":senador_despesa,
            "beneficiario":beneficiario
        }

        beneficiarioJSON.append(beneficiario)
        contrataJSON.append(contrata)

with open('JSON/Beneficiario.json','w',encoding='utf-8') as fJSON:
        json.dump(beneficiarioJSON,fJSON,ensure_ascii=False,indent=4)

with open('JSON/contrata.json','w',encoding='utf-8') as fJSON:
        json.dump(contrataJSON,fJSON,ensure_ascii=False,indent=4)
        



