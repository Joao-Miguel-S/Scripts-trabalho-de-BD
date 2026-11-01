import csv
import json

lista_parlamentar = []

with open('CSV/ListaParlamentarEmExercicio - ListaParlamentarEmExercicio.csv', 'r', encoding='UTF-8') as arquivo:
	leitor = csv.reader(arquivo, delimiter=',', quotechar='"')
	for linha in leitor:
		if linha[0] == "/ListaParlamentarEmExercicio/Parlamentares/Parlamentar/IdentificacaoParlamentar/CodigoParlamentar":
			continue
		info_senador = {
			"codSenador": int(linha[0]),
			"nome": linha[3],
			"uf": linha[10],
			"sexo": linha[4],
			"email": linha[8],
			"foto": linha[6],
			"site": linha[7],
		}
		if info_senador not in lista_parlamentar:
			if info_senador["uf"] != "":
				lista_parlamentar.append(info_senador)

with open('JSON/Senador.json','w',encoding='utf-8') as fJSON:
	json.dump(lista_parlamentar,fJSON,ensure_ascii=False,indent=4)