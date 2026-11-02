import csv
import json

def get_nome_senador(linha):
	rem = ""

	if "Gabinete do Senador " in linha:
		rem = "Gabinete do Senador "
	elif "Gabinete da Senadora " in linha:
		rem = "Gabinete da Senadora "
	elif "Escritório de Apoio nº 1 do Senador " in linha:
			rem = "Escritório de Apoio nº 1 do Senador "
	elif "Escritório de Apoio nº 1 da Senadora " in linha:
		rem = "Escritório de Apoio nº 1 da Senadora "
	elif "Escritório de Apoio nº 2 do Senador " in linha:
			rem = "Escritório de Apoio nº 2 do Senador "
	elif "Escritório de Apoio nº 2 da Senadora " in linha:
		rem = "Escritório de Apoio nº 2 da Senadora "
	
	return linha.lstrip(rem)


contador = 0
senadores = {}
servidores = []

for mes in range(1, 13):
	nome_arquivo = "CSV/Servidores/"
	nome_arquivo += f"SF_ConsultaRemuneracaoServidoresParlamentares_2025{mes:02d}.csv"
	with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:

		senadores = {}
		with open("JSON/Senador.json", 'r', encoding='utf-8') as senad:
			sen = json.load(senad)
			for s in sen:
				senadores[s["nome"]] = s["codSenador"]


		leitor = csv.reader(arquivo, delimiter=';', quotechar='"')
		for linha in leitor:
			nome_senador = get_nome_senador(linha[6])
			if nome_senador == linha[6] or nome_senador not in senadores.keys():
				continue
			servidor = {
				"codSenador": senadores[nome_senador],
				"id": contador,
				"cargo": linha[2],
				"remuneracaoBasica": linha[8],
				"remuneracaoLiquida": linha[19],
				"data": f"2025-{mes:02d}-01"
			}
			servidores.append(servidor)
			contador += 1

with open('JSON/servidores.json','w',encoding='utf-8') as fJSON:
        json.dump(servidores,fJSON,ensure_ascii=False,indent=4)