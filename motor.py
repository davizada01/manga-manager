def calcaular_lacunas(meta_volumes, volumes_adquiridos):
    if meta_volumes <= 0:
        return []
    
    todos_volumes = set(range(1, meta_volumes + 1))
    adquiridos = set(volumes_adquiridos)
    faltantes = sorted(list(todos_volumes - adquiridos))
    return faltantes

    def tem_buraco_isolado(volumes_adquiridos):
        if not volumes_adquiridos:
            return False
        
        vols = sorted(volumes_adquiridos)
        for i in range(len(vols)-1):
            if vols[i+1] - vols[i] > 1:
                return True
        return False
    
    def definir_prioridade(ficha_manga):
        if ficha_manga.get("trava_manual", False):
            return ficha_manga.get("etiqueta_prioridade", "Sem Etiqueta")
    
    score = 0
    hype = ficha_manga.get("hype", 1)
    score += (hype - 1) * 10

    status = ficha_manga.get("status", "Em Publicação")
    if status == "Finalizado":
        score += 30
    elif status == "Em Publicação":
        score += 15
    elif status == "Hiato":
        score += 10
    
    meta = ficha_manga.get("meta_volumes", 0)
    vols_adquiridos = ficha_manga.get("volumes_adquiridos", [])

    lacunas = calcaular_lacunas(meta, vols_adquiridos)

    if 0 < len(lacunas) <= 5:
        score += 20

    if tem_buraco_isolado(vols_adquiridos):
        score += 10

    if score >= 80:
        return "URGENTE"
    elif score >= 60:
        return "Alta"
    elif score >= 40:
        return "Média"
    else:
        return "Baixa"