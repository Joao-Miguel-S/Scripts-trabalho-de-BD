import json
import requests
import pandas as pd
import time
import os

def processar_lista_json(caminho):
    with open(caminho, 'r', encoding='utf-8') as f:
        senadores = json.load(f)
        
    if isinstance(senadores, dict):
        senadores = [senadores]

    headers = {"Accept": "application/json"}
    dados = []

    for i, s in enumerate(senadores, 1):
        codigo = s.get("codSenador")
        nome = s.get("nome")
        uf = s.get("uf")
        
        print(f"[{i}/{len(senadores)}] Buscando : {nome} (ID: {codigo})")
        
        url = f"https://legis.senado.leg.br/dadosabertos/senador/{codigo}/filiacoes.json"
        
        try:
            res = requests.get(url, headers=headers)
            if res.status_code == 200:
                json_filiacao = res.json()
                filiacoes = json_filiacao.get("FiliacaoParlamentar", {}).get("Parlamentar", {}).get("Filiacoes", {}).get("Filiacao", [])
    
                if isinstance(filiacoes, dict):
                    filiacoes = [filiacoes]
                    
                for f in filiacoes:
                    partido = f.get("Partido", {})
                    dados.append({
                        "CodSenador": codigo,
                        "NomeParlamentar": nome,
                        "UF": uf,
                        "CodigoPartido": partido.get("CodigoPartido", ""),
                        "SiglaPartido": partido.get("SiglaPartido", ""),
                        "NomePartido": partido.get("NomePartido", ""),
                        "DataFiliacao": f.get("DataFiliacao", ""),
                        "DataDesfiliacao": f.get("DataDesfiliacao", "")
                    })
            else:
                print(f"Erro {res.status_code} para {nome}")
                
        except Exception as e:
            print(f"Erro {nome}: {e}")
            
        time.sleep(0.1)
    
    df = pd.DataFrame(dados)
    nome_arquivo_saida = "filiacao.csv"
    
    df.to_csv(
        nome_arquivo_saida, 
        index=False, 
        sep=';', 
        encoding="utf-8-sig",
        quoting=1 
    )

if __name__ == "__main__":
    caminho_json = os.path.join("JSON", "Senador.json")
    processar_lista_json(caminho_json)