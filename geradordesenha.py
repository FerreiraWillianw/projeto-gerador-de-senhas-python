import random
import string
import os

def gerar_senha_com_padrao(tamanho, incluir_maiusculas, incluir_minusculas, incluir_numeros, incluir_especiais, embaralhar=True):
    """
    Gera uma senha aleatória com base nos critérios fornecidos.
    
    Args:
        tamanho (int): O comprimento da senha a ser gerada.
        incluir_maiusculas (bool): Se deve incluir letras maiúsculas.
        incluir_minusculas (bool): Se deve incluir letras minúsculas.
        incluir_numeros (bool): Se deve incluir números.
        incluir_especiais (bool): Se deve incluir caracteres especiais.
        embaralhar (bool): Se a senha deve ser embaralhada ou manter o padrão.
        
    Returns:
        str: A senha aleatória gerada.
    """
    # Define as listas de caracteres disponíveis
    lista_maiusculas = string.ascii_uppercase if incluir_maiusculas else []
    lista_minusculas = string.ascii_lowercase if incluir_minusculas else []
    lista_numeros = string.digits if incluir_numeros else []
    lista_especiais = string.punctuation if incluir_especiais else []

    # Combina todas as listas em uma única lista para a geração geral
    todas_as_listas = [lista_maiusculas, lista_minusculas, lista_numeros, lista_especiais]
    caracteres_disponiveis = ''.join(lista for lista in todas_as_listas if lista)
        
    # Verifica se o usuário escolheu pelo menos um tipo de caractere
    if not caracteres_disponiveis:
        return "Erro: Nenhum tipo de caractere selecionado."
    
    # Garante que a senha tenha pelo menos um de cada tipo selecionado
    senha_com_padrao = []
    
    # Adiciona um caractere de cada tipo se a lista não estiver vazia
    if lista_maiusculas:
        senha_com_padrao.append(random.choice(lista_maiusculas))
    if lista_minusculas:
        senha_com_padrao.append(random.choice(lista_minusculas))
    if lista_numeros:
        senha_com_padrao.append(random.choice(lista_numeros))
    if lista_especiais:
        senha_com_padrao.append(random.choice(lista_especiais))

    # Preenche o resto da senha com caracteres aleatórios da lista completa
    while len(senha_com_padrao) < tamanho:
        senha_com_padrao.append(random.choice(caracteres_disponiveis))
    
    # Embaralha a lista para que a ordem dos caracteres não seja previsível
    if embaralhar:
        random.shuffle(senha_com_padrao)

    # Junta os caracteres da lista em uma única string e a retorna
    return "".join(senha_com_padrao)

def salvar_senha(plataforma, senha):
    """
    Salva a senha em um arquivo, atualizando a linha se a plataforma já existir.
    """
    caminho_arquivo = "senhas.txt"
    linhas = []
    plataforma_encontrada = False

    # 1. Ler o arquivo existente (se houver) para uma lista na memória
    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, "r") as arquivo_leitura:
            linhas = arquivo_leitura.readlines()
    
    # 2. Percorrer a lista de linhas para verificar se a plataforma já existe.
    for i, linha in enumerate(linhas):
        if linha.strip().startswith(f"Plataforma: {plataforma},"):
            linhas[i] = f"Plataforma: {plataforma}, Senha: {senha}\n"
            plataforma_encontrada = True
            break

    # 3. Se a plataforma não foi encontrada, adiciona uma nova linha no final.
    if not plataforma_encontrada:
        linhas.append(f"Plataforma: {plataforma}, Senha: {senha}\n")
    
    # 4. Reescrever o arquivo com as linhas atualizadas.
    try:
        with open(caminho_arquivo, "w") as arquivo_escrita:
            arquivo_escrita.writelines(linhas)
        
        if plataforma_encontrada:
            print(f"Senha para '{plataforma}' atualizada com sucesso no arquivo 'senhas.txt'.")
        else:
            print(f"Nova senha para '{plataforma}' atualizada com sucesso no arquivo 'senhas.txt'.")

    except Exception as e:
        # Em caso de qualquer erro, exibe uma mensagem.
        print(f"Erro ao salvar senha: {e}")


if __name__ == "__main__":
    try:
        # Solicita o nome da plataforma
        plataforma = input("Para qual plataforma deseja a senha?")
        tamanho_senha = int(input("Digite o tamanho da senha desejada: "))

        # Solicita ao usuario as preferencias de caracteres ('s' para sim, 'n' para não)
        if tamanho_senha > 0:
            incluir_maiusculas = input("Incluir letras maiúsculas? (s/n) ").lower() == 's'
            incluir_minusculas = input("Incluir letras minúsculas? (s/n) ").lower() == 's'
            incluir_numeros = input("Incluir números? (s/n) ").lower() == 's'
            incluir_especiais = input("Incluir caracteres especiais? (s/n) ").lower() == 's'
            opcao_embaralhar = input("Deseja embaralhar a senha? (s/n)").lower() == 's'

            # Chama a função de geração de senha com padrão
            senha_gerada = gerar_senha_com_padrao(tamanho_senha,
                                                  incluir_maiusculas,
                                                  incluir_minusculas,
                                                  incluir_numeros,
                                                  incluir_especiais,
                                                  embaralhar=opcao_embaralhar)
            
            # Verifica se houve erro na geração da senha
            if senha_gerada.startswith("Erro: "):
                print(senha_gerada)
            else:
                print(f"Sua senha para '{plataforma}' é: {senha_gerada}")
                # Chama a função para salvar a senha
                salvar_senha(plataforma, senha_gerada)
        else:
            print("O tamanho da senha deve ser um número positivo.")

    except ValueError:
        print("Entrada inválida. Por favor, digite um número inteiro para o tamanho")
