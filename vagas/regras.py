"""Regras da DevElas: as decisões do site, escritas como funções.""" 

from datetime import date 

def minusculas(skills): 

    """Devolve uma lista nova com as skills em letras minúsculas.""" 

    resultado = [] 

    for skill in skills: 

        resultado.append(skill.lower()) 

    return resultado 

def compatibilidade(skills_da_vaga, minhas_skills): 

    """Devolve, de 0 a 100, quanto as minhas skills combinam com as da vaga. 

    Maiúsculas e minúsculas não importam: "python" conta como "Python". 

    Exemplo: a vaga pede Python, SQL e Excel, e eu tenho Python e Excel. 

    São 2 de 3, então a função devolve 66. 

    Se a vaga não pedir nenhuma skill, devolve 0. 

    """ 

    if not skills_da_vaga: 

        return 0 

    minhas = minusculas(minhas_skills) 

    acertos = 0 

    for skill in skills_da_vaga: 

        if skill.lower() in minhas: 

            acertos += 1 

    return acertos * 100 // len(skills_da_vaga) 

def skills_que_faltam(skills_da_vaga, minhas_skills): 

    """Devolve a lista das skills da vaga que eu ainda não tenho. 

    Exemplo: a vaga pede Python, SQL e Excel, e eu tenho Python e Excel. 

    A função devolve ["SQL"]. 

    """ 

    minhas = minusculas(minhas_skills) 

    faltam = [] 

    for skill in skills_da_vaga: 

        if skill.lower() not in minhas: 

            faltam.append(skill) 

    return faltam 

def vaga_aberta(vaga, hoje=None): 

    """Devolve True se a vaga ainda aceita candidaturas, e False se já encerrou. 

    A vaga fica aberta até o dia do prazo, inclusive. 

    O parâmetro hoje serve para testar com outra data; sem ele, vale a data de hoje. 

    """ 

    if hoje is None: 

        hoje = date.today() 

    return vaga["prazo"] >= hoje 