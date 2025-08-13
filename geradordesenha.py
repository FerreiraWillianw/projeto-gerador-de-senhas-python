import random
import string
import pandas as pd

def gerar_senha_com_padrao(tamanho, incluir_maiusculas, incluir_minusculas, incluir_numeros, incluir_especiais, embaralhar=True):
    """
    Gera uma senha aleatória com um padrão, garantindo que pelo menos um
    caractere de cada tipo selecionado seja incluído.
    """
    # Cria listas com os caracteres disponíveis, se a opção do usuário for 'True'.
    # Caso contrário, a lista fica vazia.
    lista_maiusculas = string.ascii_uppercase if incluir_maiusculas else []
    lista_minusculas = string.ascii_lowercase if incluir_minusculas else []
    lista_numeros = string.digits if incluir_numeros else []
    lista_especiais = string.punctuation if incluir_especiais else []

    # Junta todas as listas para ter um conjunto completo de caracteres
    todas_as_listas = [lista_maiusculas, lista_minusculas, lista_numeros, lista_especiais]
    caracteres_disponiveis = ''.join(lista for lista in todas_as_listas if lista)
        
    # #Verifica se o usuário escolheu pelo menos uma opção.
    if not caracteres_disponiveis:
        return "Erro: Nenhum tipo de caractere selecionado."
    
    senha_com_padrao = []
    
    # #Garante que a senha tenha pelo menos um de cada tipo, se selecionado.
    if lista_maiusculas:
        senha_com_padrao.append(random.choice(lista_maiusculas))
    if lista_minusculas:
        senha_com_padrao.append(random.choice(lista_minusculas))
    if lista_numeros:
        senha_com_padrao.append(random.choice(lista_numeros))
    if lista_especiais:
        senha_com_padrao.append(random.choice(lista_especiais))

    # #Preenche o restante da senha até atingir o tamanho desejado.
    while len(senha_com_padrao) < tamanho:
        senha_com_padrao.append(random.choice(caracteres_disponiveis))
    
    # #Embaralha a lista para que a senha não tenha um padrão fixo, se o usuário optou por isso.
    if embaralhar:
        random.shuffle(senha_com_padrao)

    # #Converte a lista de caracteres em uma única string e a retorna.
    return "".join(senha_com_padrao)

def salvar_senha(plataforma, senha):
    """
    Salva a senha em um arquivo Excel, atualizando a linha se a plataforma já existir.
    """
    caminho_arquivo = "senhas.xlsx"
    
    try:
        # #Tenta ler o arquivo Excel. Se não existir, a exceção é capturada.
        df = pd.read_excel(caminho_arquivo)
    except FileNotFoundError:
        # #Se o arquivo não existir, cria um novo DataFrame com as colunas 'Plataforma' e 'Senha'.
        df = pd.DataFrame(columns=['Plataforma', 'Senha'])
    
    # #Usa indexação booleana (método mais eficiente) para encontrar a linha da plataforma.
    linha_existente = df[df['Plataforma'] == plataforma]
    
    if not linha_existente.empty:
        # #Se a plataforma existe, atualiza a senha na linha correspondente.
        df.loc[linha_existente.index, 'Senha'] = senha
        print(f"Senha para '{plataforma}' atualizada com sucesso no arquivo '{caminho_arquivo}'.")
    else:
        # #Se não existe, cria uma nova linha com os dados.
        nova_linha = pd.DataFrame([{'Plataforma': plataforma, 'Senha': senha}])
        # #Adiciona a nova linha ao final do DataFrame.
        df = pd.concat([df, nova_linha], ignore_index=True)
        print(f"Nova senha para '{plataforma}' salva com sucesso no arquivo '{caminho_arquivo}'.")
        
    try:
        # #Salva o DataFrame atualizado de volta no arquivo Excel.
        df.to_excel(caminho_arquivo, index=False)
    except Exception as e:
        print(f"Erro ao salvar a senha no Excel: {e}")

def main():
    """
    Função principal que lida com a interação do usuário e a lógica do programa.
    """
    try:
        plataforma = input("Para qual plataforma você deseja a senha? ")
        tamanho_senha = int(input("Digite o tamanho da senha desejada: "))

        if tamanho_senha <= 0:
            print("O tamanho da senha deve ser um número positivo.")
            return

        incluir_maiusculas = input("Incluir letras maiúsculas? (s/n) ").lower() == 's'
        incluir_minusculas = input("Incluir letras minúsculas? (s/n) ").lower() == 's'
        incluir_numeros = input("Incluir números? (s/n) ").lower() == 's'
        incluir_especiais = input("Incluir caracteres especiais? (s/n) ").lower() == 's'
        opcao_embaralhar = input("Deseja embaralhar a senha para maior segurança? (s/n) ").lower() == 's'
        
        # #Valida se o usuário selecionou pelo menos um tipo de caractere.
        if not (incluir_maiusculas or incluir_minusculas or incluir_numeros or incluir_especiais):
            print("Erro: Nenhum tipo de caractere selecionado. A senha não pode ser gerada.")
            return

        senha_gerada = gerar_senha_com_padrao(tamanho_senha,
                                              incluir_maiusculas,
                                              incluir_minusculas,
                                              incluir_numeros,
                                              incluir_especiais,
                                              embaralhar=opcao_embaralhar)
        
        # #Exibe a senha e a salva no Excel, usando a função salvar_senha.
        print(f"Sua senha para '{plataforma}' é: {senha_gerada}")
        salvar_senha(plataforma, senha_gerada)

    except ValueError:
        print("Entrada inválida. Por favor, digite um número inteiro para o tamanho.")

#A linha principal do programa, que executa a função 'main()' quando o script é rodado.
if __name__ == "__main__":
    main()
