import json
from types import SimpleNamespace

query = []
with open('JSON/Senador.json',"r") as file:
        create = "CREATE TABLE Senador (codSenador INT, nome VARCHAR(70), uf CHAR(2), sexo VARCHAR(20), email VARCHAR(50),  foto VARCHAR(100), site VARCHAR(100)" \
        "PRIMARY KEY(codSenador));"
        query.append(create)
        data = json.load(file)

        with open('SQL/Senador.sql','w',encoding='utf-8') as f:
            for senador in data:
                insert = "INSERT INTO Senador values ({0},'{1}','{2}','{3}','{4}','{5}','{6}');\n".format(senador["codSenador"],senador["nome"], senador["uf"],senador["sexo"],senador["email"],senador["foto"],senador["site"])
                f.write(insert)
        



