from django.http import Http404 

from django.shortcuts import render 

from vagas.dados import MINHAS_SKILLS, ler_vagas_csv 

from vagas.regras import compatibilidade, skills_que_faltam, vaga_aberta 

def vagas_com_regras(): 

    """Lê as vagas do CSV e acrescenta, em cada uma, o resultado das regras.""" 

    vagas = ler_vagas_csv() 

    for vaga in vagas: 

        vaga["aberta"] = vaga_aberta(vaga) 

        vaga["compatibilidade"] = compatibilidade(vaga["skills"], MINHAS_SKILLS) 

        vaga["faltam"] = skills_que_faltam(vaga["skills"], MINHAS_SKILLS) 

    return vagas 

def home(request): 

    abertas = [] 

    for vaga in vagas_com_regras(): 

        if vaga["aberta"]: 

            abertas.append(vaga) 

    return render(request, "vagas/home.html", {"total": len(abertas)}) 

def mural(request): 

    modalidade = request.GET.get("modalidade", "") 

    vagas = vagas_com_regras() 

    if modalidade: 

        filtradas = [] 

        for vaga in vagas: 

            if vaga["modalidade"] == modalidade: 

                filtradas.append(vaga) 

        vagas = filtradas 

    contexto = { 

        "vagas": vagas, 

        "total": len(vagas), 

        "modalidade": modalidade, 

    } 

    return render(request, "vagas/mural.html", contexto) 

def detalhe(request, vaga_id): 

    for vaga in vagas_com_regras(): 

        if vaga["id"] == vaga_id: 

            return render(request, "vagas/detalhe.html", {"vaga": vaga}) 

    raise Http404("Vaga não encontrada") 

def sobre(request): 

    vagas = ler_vagas_csv() 

    empresas = [] 

    for vaga in vagas: 

        if vaga["empresa"] not in empresas: 

            empresas.append(vaga["empresa"]) 

    contexto = { 

        "total": len(vagas), 

        "empresas": len(empresas), 

    } 

    return render(request, "vagas/sobre.html", contexto) 

def contato(request): 

    return render(request, "vagas/contato.html") 