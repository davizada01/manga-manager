import gerenciador
import motor

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

    for titulo, dados in obras.items():
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
    print("\n---Cadastrar Obra Nova---")
    titulo = input("Nome da Obra: ").strip()
    autor = input("Nome do Autor: ").strip()
    editora = input("Editora: ").strip()

    print("\nStatus: [1] Em Publicação  [2] Finalizado  [3] Hiato")
    opcao_status = input("Qual status da obra (1/2/3): ").strip()
    mapa_status = {"1": "Em Publicação", "2": "Finalizado", "3": "Hiato"}
    status = mapa_status.get(opcao_status, "Em Publicação")

    meta = int(input("Meta de Volumes Atual: "))

    print("\nSe for um desejo que você ainda não tem nada, digite 0.")
    vols_str = input("Quais volumes você já tem? (Separe por vírgula. Ex.: 1,2,3): ")

    if vols_str.strip() == 0:
        volumes = []
    else:
        volumes = [int(v.strip()) for v in vols_str.split(",") if v.strip().isdigit()]

    hype = int(input("Seu nível de Hype (1 e 5): "))

    nova_obra = {
        "titulo": titulo,
        "autor": autor,
        "editora": editora,
        "status": status,
        "meta_volumes": meta,
        "volumes_adquiridos": volumes,
        "hype": hype,
        "prioridade_editada": False
    }

    gerenciador.cadastrar_obra(nova_obra)
    print(f"\n '{titulo}' cadastrado com sucesso!")

def detalhes_obra(obra):
    titulo = obra["titulo"]
    print("\n" + "="*35)
    print(f"DETALHES: {titulo.upper()}")
    print(f"Autor: {obra.get('autor')} | Editora: {obra.get('editora')}")
    print(f"Status: {obra.get('status')}")
    print(f"Hype: {obra.get('hype')}/5")
    print(f"Volumes na mão: {obra.get('volumes_adquiridos')}")
    print(f"Meta de volumes: {obra.get('meta_volumes')}")
    print(f"Etiqueta Atual: {obra.get('etiqueta_prioridade')}")

    if obra.get("prioridade_editada"):
        print("Prioridade Editada Manualmente")
    print("="*35)

    print("\n[1] Alterar Etiqueta")
    print("[2] Voltar")

    acao = input("O que deseja fazer? ").strip()

    if acao == "1":
        nova_etiqueta = input("Digite a Nova etiqueta exata (Ex.: Dropado, Máxima): ")
        gerenciador.aplicar_override(titulo, nova_etiqueta)
        print("Etiqueta automática removida. O motor não mexe mais aqui.")

def ver_estante():
    obras = gerenciador.listar_todas_obras()
    estante = {k: v for k, v in obras.items() if len(v.get("volumes_adquiridos", [])) > 0}

    if not estante:
        print("\nSua estante está vazia.")
        return
    
    print("\n--- SUA ESTANTE COMPLETA ---")
    for titulo, dados in estante.items():
        print(f"{titulo} | Prioridade: {dados.get('etiqueta_prioridade')}")

    escolha = input("\nDigite o número exato da obra para ver os detalhes ou editar a prioridade (ou ENTER para voltar): ").strip()

    if escolha in estante:
        detalhes_obra(estante[escolha])
    elif escolha:
        print("Obra não encontrada.")

def ver_wishlist():
    obras = gerenciador.listar_todas_obras()
    wishlist = {k: v for k, v in obras.items() if len (v.get("volumes_adquiridos", [])) == 0}
    
    if not wishlist:
        print("\nSua Wishlist está vazia.")
        return
    
    print("\n---WISHLIST---")
    for titulo, dados in wishlist.items():
        print(f"- {titulo} | Hype: {dados.get('hype')}/5 | Meta: {dados.get('meta_volumes')} vols")

    input("\nPressione ENTER para voltar. ")

def main():
    while True:
        exibir_menu()
        opcao = input("Escolha o que quer fazer: ").strip()

        if opcao == "1":
            painel_compras()
        elif opcao == "2":
            atualizar_rapido()
        elif opcao == "3":
            ver_estante()
        elif opcao == "4":
            cadastrar_tela()
        elif opcao == "5":
            ver_wishlist()
        elif opcao == "6":
            print("\nFechando...")
            break
        else:
            print("\nComando inválido. Tente novamente.")

if __name__ == "__main__":
    main()
