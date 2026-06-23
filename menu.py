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
    
    obras = gerenciador.listar_todas_obras()
    lista_titulos = list(obras.keys())

    if not lista_titulos:
        print("Nenhuma obra cadastrada pra ser atualizada.")
        return
    
    for i, titulo in enumerate(lista_titulos):
        print(f"[{i + 1}] {titulo}")

    escolha = input("\nQual obra chegou? (Digite o NÚMERO ou ENTER para voltar): ").strip()

    if escolha == "":
        return
    
    if escolha.isdigit():
        indice = int(escolha) - 1
        if 0 <= indice < len(lista_titulos):
            titulo = lista_titulos[indice]

            vols_str = input(f"Quais volumes novos de '{titulo}' você comprou? (Separados por vírgula): ")
            novos = [int(v.strip)() for v in vols_str.split(",") if v.strip().isdigit()]

            if novos:
                gerenciador.atualizar_volumes(titulo, novos)
                print(f"Sucesso! Volumes de '{titulo}' atualizados.")
                print(f"A prioridade '{titulo}' já foi recalculada automáticamente!!")
            else:
                print("Nenhum volume válido digitado.")
        else:
            print("Número não foi encontrado na lista.")
    else:
        print("Por favor, digite apenas números.")



def cadastrar_tela():
    print("\n---Cadastrar Obra Nova---")
    titulo = input("Nome da Obra: ").strip()
    autor = input("Nome do Autor: ").strip()
    editora = input("Editora: ").strip()

    print("\nStatus: [1] Em Publicação  [2] Finalizado  [3] Hiato")
    opcao_status = input("Qual status da obra (1/2/3): ").strip()
    mapa_status = {"1": "Em Publicação", "2": "Finalizado", "3": "Hiato"}
    status = mapa_status.get(opcao_status, "Em Publicação")

    if status == "Finalizado":
        mensagem_meta = "Quantos volumes totais a obra tem? "
    elif status == "Hiato":
        mensagem_meta = "Em qual volume a obra parou? "
    else:
        mensagem_meta = "Quantos volumes já lançaram? "

    while True:
        try:
            meta = int (input(mensagem_meta))
            break
        except ValueError:
            print("Erro: Digite apenas o número único (Ex.: 25)")

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
    
    lista_titulos = list (estante.keys())
    
    for i, titulo in enumerate(lista_titulos):
        dados = estante[titulo]
        etiqueta = dados.get('etiqueta_prioridade')

        vols_na_mao = len(dados.get('volumes_adquiridos', []))
        meta = dados.get('meta_volumes', 0)

        if meta > 0:
            progresso = f"{vols_na_mao}/{meta}"
        else:
            progresso = f"{vols_na_mao}/?"

        if etiqueta == "Completo!":
            print(f"[{i + 1}] {titulo} | Completo!")
        else:
            print(f"[{i + 1}] {titulo} | Prioridade: {etiqueta}")
    
    escolha = input("\nDigite o número da obra para ver detalhes (ou ENTER para voltar): ").strip()

    if escolha == "":
        return

    if escolha.isdigit():
        indice = int(escolha) - 1

        if 0 <= indice < len(lista_titulos):
            titulo_escolhido = lista_titulos[indice]
            detalhes_obra(estante[titulo_escolhido])
        else:
            print("Número não encontrado na lista.")
    else:
        print("Por favor, digite NÚMEROS.")

def ver_wishlist():
    obras = gerenciador.listar_todas_obras()
    wishlist = {k: v for k, v in obras.items() if len (v.get("volumes_adquiridos", [])) == 0}
    
    if not wishlist:
        print("\nSua Wishlist está vazia.")
        return
    
    print("\n---WISHLIST---")
    lista_titulos = list(wishlist.keys())
    for i, titulo in enumerate(lista_titulos):
        dados = wishlist[titulo]
        print(f"[{i + 1}] {titulo} | Hype: {dados.get('hype')}/5 | Meta: {dados.get('meta_volumes')} vols")

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
