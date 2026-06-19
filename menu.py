import gerenciador

def exibir_menu():
    print("\n" + "="*45)
    print("Mangá Manager")
    print("="*45)
    print("[1] Painel de Compras")
    print("[2] Volumes Novos")
    print("[3] Estante Completa e Detalhes")
    print("[4] Cadastrar Nova Obra")
    print("[5] Wishlist")
    print("[6] Sair")
    print("="*45)

def painel_compras():
    obras = gerenciador.listar_todas_obras()

    alvos_urgentes = []
    alvos_altos = []

    for titulo, dados in obras.itens():
        if len(dados.get("volumes_adquiridos", [])) > 0:
            etiqueta = dados.get("etiqueta_prioridade", "")
            if "URGENTE" in etiqueta:
                alvos_urgentes.append((titulo, dados))
            elif "Alta" in etiqueta:
                alvos_altos.append((titulo, dados))

    print("\n" + "!"*45)
    print("FOCO MÁXIMO (URGENTES)")
    if not alvos_urgentes:
        print("Nenhuma obra urgente!")
    else: 
        for titulo, dados in alvos_urgentes:
            lacunas = motor.calcular_lacunas(dados["meta_volumes"]), dados ["volumes_adquiridos"]
            proximos = lacunas[:3]
            print(f"- {titulo} | Faltam os vols: {proximos}...")
    
    print("\n" + "-"*45)
    print("Próximos da Fila")
    if not alvos_altos:
        print("Nenhuma obra com prioridade alta no radar.")
    else:
        for titulo, dados in alvos_altos:
            lacunas = motor.calcular_lacunas(dados["meta_volumes"], dados["volumes_adquiridos"])
            proximos = lacunas[:3]
            print(f"- {titulo} | Faltam os vols: {proximos}...")
    print("!" *45)
    input ("\n Pressione ENTER para voltar ao menu.")

def atualizar_rapido():
    print("\n--- Dar Baixa em Compras---")
    titulo = input("Qual obra chegou? (Digite o nome exato!): ").strip()

    obras = gerenciador.listar_todas_obras()
    if titulo not in obras:
        print("Obra não Encotrada. Verifique o nome na Estante.")
        return
    
    vols_str = input(f"Quais volumes novos de {titulo} você comprou? (Separe com vírgula): ")
    novos = [int(v.strip()) for v in vols_str.split(",") if v.strip().isdigit()]

    if novos:
        gerenciador.atualizar_volumes(titulo, novos)
        print(f"Sucesso! Volumes de '{titulo} atualizados.")
        print("A etiqueta de prioridade dessa obra foi atualizada automaticamente!")
    else:
        print("Nenhum volume válido digitado.")

def cadastrar_tela():