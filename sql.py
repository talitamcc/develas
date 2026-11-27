"""Console de consultas SQL da DevElas: só lê o banco, nunca muda nada. 

Rode com:  python sql.py 

Digite uma consulta e aperte Enter. Atalhos: tabelas (lista as tabelas) e sair. 

""" 

import sqlite3 

from pathlib import Path 

BANCO = Path(__file__).resolve().parent / "db.sqlite3" 

LARGURA_MAXIMA = 40 

LISTAR_TABELAS = "SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name" 

def encurtar(valor): 

    """Transforma o valor em texto e corta textos compridos, para caber na tela.""" 

    if valor is None: 

        return "" 

    texto = str(valor) 

    if len(texto) > LARGURA_MAXIMA: 

        return texto[:LARGURA_MAXIMA - 1] + "…" 

    return texto 

def mostrar(cursor): 

    """Mostra o resultado de uma consulta como uma tabela de texto.""" 

    colunas = [] 

    for coluna in cursor.description: 

        colunas.append(coluna[0]) 

    linhas = [] 

    for linha in cursor.fetchall(): 

        celulas = [] 

        for valor in linha: 

            celulas.append(encurtar(valor)) 

        linhas.append(celulas) 

    larguras = [] 

    for posicao, nome in enumerate(colunas): 

        maior = len(nome) 

        for linha in linhas: 

            maior = max(maior, len(linha[posicao])) 

        larguras.append(maior) 

    def formatar(celulas): 

        partes = [] 

        for posicao, texto in enumerate(celulas): 

            partes.append(texto.ljust(larguras[posicao])) 

        return " | ".join(partes) 

    print(formatar(colunas)) 

    print("-+-".join("-" * largura for largura in larguras)) 

    for linha in linhas: 

        print(formatar(linha)) 

    print(f"({len(linhas)} linha(s))\n") 

def main(): 

    if not BANCO.exists(): 

        print("O db.sqlite3 ainda não existe. Rode antes:  python manage.py migrate") 

        return 

    conexao = sqlite3.connect(BANCO.as_uri() + "?mode=ro", uri=True) 

    print("Console SQL da DevElas (só leitura). Atalhos: tabelas, sair.\n") 

    while True: 

        try: 

            consulta = input("sql> ").strip() 

        except (EOFError, KeyboardInterrupt): 

            break 

        if consulta.lower() == "sair": 

            break 

        if not consulta: 

            continue 

        if consulta.lower() == "tabelas": 

            consulta = LISTAR_TABELAS 

        try: 

            mostrar(conexao.execute(consulta)) 

        except sqlite3.OperationalError as erro: 

            if "readonly" in str(erro): 

                print("Este console só lê o banco. Para mudar dados, use o admin.") 

                print() 

            else: 

                print(f"O SQL não entendeu: {erro}\n") 

        except sqlite3.Error as erro: 

            print(f"Ops: {erro}\n") 

    conexao.close() 

    print("Até a próxima consulta!") 

main() 