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
    print("\n--- PAINEL DE COMPRAS ---")
    obras = gerenciador.listar_todas_obras()
    
    if not obras:
        print("Nenhum mangá cadastrado no sistema.")
        return

    fila_urgente = []
    fila_alta = []
    fila_media = []
    fila_baixa = []

    for titulo, dados in obras.items():
        vols_na_mao = len(dados.get('volumes_adquiridos', []))
        meta = dados.get('meta_volumes', 0)
        etiqueta = str(dados.get("etiqueta_prioridade", ""))
        
        if (meta > 0 and vols_na_mao >= meta) or "completo" in etiqueta.lower() or "dropado" in etiqueta.lower():
            continue
            
        progresso = f"{vols_na_mao}/{meta}" if meta > 0 else f"{vols_na_mao}/?"
        linha_manga = f"{titulo} ({progresso})"

        etiqueta_minuscula = etiqueta.lower()

        if "urgente" in etiqueta_minuscula:
            fila_urgente.append(f"Urgente  | {linha_manga}")
        elif "alta" in etiqueta_minuscula:
            fila_alta.append(f"Alta     | {linha_manga}")
        elif "media" in etiqueta_minuscula or "media" in etiqueta_minuscula:
            fila_media.append(f"Média    | {linha_manga}")
        else:
            fila_baixa.append(f"Baixa    | {linha_manga}")

    lista_final = fila_urgente + fila_alta + fila_media + fila_baixa

    if not lista_final:
        print("Tudo atualizado! Nenhuma compra pendente no radar.")
    else:
        for item in lista_final:
            print(item)
            
    print("-" * 45)
    input("Pressione ENTER para voltar ao menu: ")
    
def atualizar_rapido():
    print("\n--- Dar Baixa em Compras---")

    obras = gerenciador.listar_todas_obras()
    
    lista_titulos = []
    for titulo, dados in obras.items():
        vols_na_mao = len(dados.get('volumes_adquiridos', []))
        meta = dados.get('meta_volumes', 0)
        etiqueta = str(dados.get("etiqueta_prioridade", ""))
        
        if (meta > 0 and vols_na_mao >= meta) or "completo" in etiqueta.lower() or "dropado" in etiqueta.lower():
            continue
        lista_titulos.append(titulo)

    if not lista_titulos:
        print("Nenhuma obra pendente pra ser atualizada.")
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
            novos = [int(v.strip()) for v in vols_str.split(",") if v.strip().isdigit()]

            if novos:
                gerenciador.atualizar_volumes(titulo, novos)
                print(f"Sucesso! Volumes de '{titulo}' atualizados.")
                print(f"A prioridade '{titulo}' já foi recalculada automaticamente!!")
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
    genero_str = input("Gêneros (Separe por vírgula): ").strip()
    genero = [g.strip().title() for g in genero_str.split(",")] if genero_str else[]
    ano = input("Período de Lançamento (Ex.: 1999 - Atual, 2015 - 2025): ").strip()

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

    if vols_str.strip() == "0":
        volumes = []
    else:
        volumes = [int(v.strip()) for v in vols_str.split(",") if v.strip().isdigit()]

    if meta > 0 and len (volumes) >= meta:
        hype = 1
    else:
        hype = int(input("Seu nível de Hype (1 e 5): "))

    nova_obra = {
        "titulo": titulo,
        "autor": autor,
        "editora": editora,
        "genero": genero,
        "ano_lancamento": ano, 
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
    print(f"Gênero: {obra.get('genero', 'Não definido')}")
    print(f"Período de Lançamento: {obra.get('ano_lancamento', 'Não definido')}")
    print(f"Autor: {obra.get('autor')} | Editora: {obra.get('editora')}")
    print(f"Status: {obra.get('status')}")

    etiqueta_atual = str(obra.get("etiqueta_prioridade", "")).lower()
    if "completo" not in etiqueta_atual:
        print(f"Hype: {obra.get('hype')}/5")
    
    print(f"Volumes na mão: {obra.get('volumes_adquiridos', [])}")
    
    buracos = gerenciador.obter_lacunas(obra)
    if buracos:
        print(f"Buracos na Coleção: {buracos}")

    print(f"Meta de volumes: {obra.get('meta_volumes')}")
    print(f"Etiqueta Atual: {obra.get('etiqueta_prioridade')}")

    if obra.get("prioridade_editada"):
        print("Prioridade Editada Manualmente")
    print("="*35)

    print("\n[1] Editar Detalhes")
    print("[2] Alterar Etiqueta Manualmente")
    print("[3] Deletar Obra")
    print("[4] Voltar")

    acao = input("O que deseja fazer? ").strip()

    if acao == "1":
        print("\n=== Editando: {titulo} ===")
        print("(Aperte ENTER sem digitar nada para manter o valor atual)")

        generos_atuais = obra.get('genero', [])
        textos_generos_atuais = ", ".join(generos_atuais) if isinstance(generos_atuais, list) else generos_atuais

        novo_genero_str = input(f"Gêneros atuais ({textos_generos_atuais})[separe por vírgula]: ").strip()
        novo_ano = input(f"Época atual ({obra.get('ano_lancamento', 'Não definido')}): ").strip()
        novo_meta = input(f"Último Volume lançado / Meta atual ({obra.get('meta_volumes')}): ").strip()
        novo_status = input(f"Status Atual ({obra.get('status')}): ").strip()

        novos_dados = {}
        if novo_genero: novos_dados["genero"] = novo_genero
        if novo_ano: novos_dados["ano_lancamento"] = novo_ano
        if novo_status: novos_dados["status"] = novo_status
        if novo_meta.isdigit(): novos_dados["meta_volumes"] = int(novo_meta)

        if novos_dados:
            gerenciador.editar_detalhes_obra(titulo, novos_dados)
            print("Detalhes atualizados com sucesso!")
        else: 
            print("Nenhuma alteração foi feita.")

    if acao == "2":
        nova_etiqueta = input("Digite a Nova etiqueta exata (Ex.: Dropado, Máxima ou alguma existente: : ")
        gerenciador.editar_prioridade(titulo, nova_etiqueta)
        print("Etiqueta automática removida. O motor não mexe mais aqui.")

    if acao == "3":
        certeza = input(f"Tem certeza que deseja DELETAR '{titulo}? (S/N): ").strip().upper()
        if certeza == "S":
            gerenciador.deletar_obra(titulo)
            print(f"\nObra'{titulo}' deletada.")

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
            print(f"[{i + 1}] {titulo} ({progresso}) | Completo!")
        elif "dropado" in str(etiqueta).lower():
            print(f"[{i + 1}] {titulo} ({progresso}) | Dropado")
        else:
            print(f"[{i + 1}] {titulo} ({progresso}) | Prioridade: {str(etiqueta).title()}")
    
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
