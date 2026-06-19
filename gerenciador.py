import database
import motor

def cadastrar_obra(nova_obra):
    acervo = database.carregar_acervo
    titulo = nova_obra["titulo"]

    etiqueta = motor.definir_prioridade(nova_obra)
    nova_obra["etiqueta_prioridade"] = etiqueta

    acervo[titulo] = nova_obra
    database.salvar_acervo(acervo)

    return True

def listar_todas_obras():
    return database.carregar_acervo()

def atualizar_volumes(titulo, novos_volumes):
    acervo = database.carregar_acervo
    
    if titulo in acervo:
        obra = acervo[titulo]

        todos_volumes = set(obra.get("volumes_adquiridos", []) + novos_volumes)
        obra["volumes_adquiridos"] = sorted(list(todos_volumes))

        obra["etiqueta_prioridade"] = motor.definir_prioridade(obra)

        database.salvar_acervo(acervo)
        return True
    return database

def atualizar_volumes(titulo, novos_volumes):
    acervo = database.carregar_acervo()

    if titulo in acervo:
        obra = acervo[titulo]
        todos_volumes = set(obra.get("volumes_adquiridos", []) + novos_volumes)
        obra["volumes_adquridos"] = sorted(list(todos_volumes))

        obra["etiqueta_prioridade"] = motor.definir_prioridade(obra)

        database.salvar_acervo(acervo)
        return True
    return False

def aplicar_override(titulo, nova_prioridade):
    acervo = database.carregar_acervo()

    if titulo in acervo:
        obra = acervo [titulo]
        obra["trava_manual"] = True
        obra["etiqueta_prioridade"] = nova_prioridade

        database.salvar_acervo(acervo)
        return True
    return False
