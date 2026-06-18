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
