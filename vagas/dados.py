"""Dados da DevElas: as vagas agora moram no arquivo vagas.csv.""" 

import csv 

from datetime import date 

from pathlib import Path 

 

CAMINHO_CSV = Path(__file__).resolve().parent / "vagas.csv" 

 

# Troque pelas suas 5 skills (a missão da aula 6) 

MINHAS_SKILLS = ["Python", "HTML", "Git", "Comunicação", "Excel"] 

 

 

def abrir_csv(caminho): 

    """Devolve o texto do arquivo, venha ele do editor (UTF-8) ou do Excel.""" 

    try: 

        return Path(caminho).read_text(encoding="utf-8-sig") 

    except UnicodeDecodeError: 

        return Path(caminho).read_text(encoding="cp1252") 

 

 

def montar_vaga(linha): 

    """Transforma uma linha do CSV num dicionário de vaga, com os tipos certos.""" 

    skills = [] 

    for skill in linha["skills"].split(","): 

        if skill.strip(): 

            skills.append(skill.strip()) 

 

    return { 

        "id": int(linha["id"]), 

        "titulo": linha["titulo"], 

        "empresa": linha["empresa"], 

        "cidade": linha["cidade"], 

        "area": linha["area"], 

        "nivel": linha["nivel"], 

        "modalidade": linha["modalidade"], 

        "skills": skills, 

        "prazo": date.fromisoformat(linha["prazo"]), 

        "descricao": linha["descricao"], 

    } 

 

 

def ler_vagas_csv(caminho=CAMINHO_CSV): 

    """Lê o CSV e devolve a lista de vagas, uma por linha. 

 

    Se o arquivo não existir, avisa no terminal e devolve uma lista vazia. 

    Linhas com id ou prazo em formato errado são puladas, também com aviso. 

    """ 

    try: 

        texto = abrir_csv(caminho) 

    except FileNotFoundError: 

        print(f"Aviso: o arquivo {caminho} não foi encontrado.") 

        return [] 

 

    vagas = [] 

    linhas = csv.DictReader(texto.splitlines(), delimiter=";") 

    for numero, linha in enumerate(linhas, start=2): 

        try: 

            vagas.append(montar_vaga(linha)) 

        except (KeyError, TypeError, ValueError) as erro: 

            print(f"Aviso: a linha {numero} do vagas.csv foi pulada ({erro}).") 

    return vagas 