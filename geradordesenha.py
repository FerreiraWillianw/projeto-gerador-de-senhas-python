import random
import string
import pandas as pd
import tkinter as tk

def gerar_senha_com_padrao(tamanho, incluir_maiusculas, incluir_minusculas, incluir_numeros, incluir_especiais, embaralhar=True):
    """
    Gera uma senha aleatória com um padrão, garantindo que pelo menos um
    caractere de cada tipo selecionado seja incluído.
    """
    lista_maiusculas = string.ascii_uppercase if incluir_maiusculas else []
    lista_minusculas = string.ascii_lowercase if incluir_minusculas else []
    lista_numeros = string.digits if incluir_numeros else []
    lista_especiais = string.punctuation if incluir_especiais else []
    todas_as_listas = [lista_maiusculas, lista_minusculas, lista_numeros, lista_especiais]
    caracteres_disponiveis = ''.join(lista for lista in todas_as_listas if lista)
    if not caracteres_disponiveis:
        return "Erro: Nenhum tipo de caractere selecionado."
    senha_com_padrao = []
    if lista_maiusculas:
        senha_com_padrao.append(random.choice(lista_maiusculas))
    if lista_minusculas:
        senha_com_padrao.append(random.choice(lista_minusculas))
    if lista_numeros:
        senha_com_padrao.append(random.choice(lista_numeros))
    if lista_especiais:
        senha_com_padrao.append(random.choice(lista_especiais))
    while len(senha_com_padrao) < tamanho:
        senha_com_padrao.append(random.choice(caracteres_disponiveis))
    if embaralhar:
        random.shuffle(senha_com_padrao)
    return "".join(senha_com_padrao)

def salvar_senha(plataforma, senha):
    """
    Salva a senha em um arquivo Excel, atualizando a linha se a plataforma já existir.
    """
    caminho_arquivo = "senhas.xlsx"
    try:
        df = pd.read_excel(caminho_arquivo)
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Plataforma', 'Senha'])
    linha_existente = df[df['Plataforma'] == plataforma]
    mensagem_status = ""
    if not linha_existente.empty:
        df.loc[linha_existente.index, 'Senha'] = senha
        mensagem_status = f"Senha para '{plataforma}' atualizada com sucesso."
    else:
        nova_linha = pd.DataFrame([{'Plataforma': plataforma, 'Senha': senha}])
        df = pd.concat([df, nova_linha], ignore_index=True)
        mensagem_status = f"Nova senha para '{plataforma}' salva com sucesso."
    try:
        df.to_excel(caminho_arquivo, index=False)
        return mensagem_status
    except Exception as e:
        print(f"Erro ao salvar a senha no Excel: {e}")

def gerar_senha_gui(entrada_tamanho, var_maiusculas, var_minusculas, var_numeros, var_especiais, var_embaralhar, exibir_senha, label_feedback):
    """
    Função que será chamada pelo botão para gerar a senha.
    """
    try:
        tamanho_senha = int(entrada_tamanho.get())
        if tamanho_senha <= 0:
            exibir_senha.delete(0, tk.END)
            exibir_senha.insert(0, "Erro: Tamanho inválido!")
            label_feedback.config(text="Erro: Tamanho inválido!", fg="red")
            return

        incluir_maiusculas = var_maiusculas.get()
        incluir_minusculas = var_minusculas.get()
        incluir_numeros = var_numeros.get()
        incluir_especiais = var_especiais.get()
        embaralhar_senha = var_embaralhar.get()

        senha_gerada = gerar_senha_com_padrao(tamanho_senha, incluir_maiusculas, incluir_minusculas,
                                              incluir_numeros, incluir_especiais, embaralhar_senha)
        
        # Chama a nova função de validação de força
        forca_senha = verificar_forca_senha(senha_gerada)

        exibir_senha.delete(0, tk.END)
        exibir_senha.insert(0, senha_gerada)
        
        # Exibe o status de força da senha
        if forca_senha == "Forte":
            cor = "green"
        elif forca_senha == "Média":
            cor = "orange"
        else:
            cor = "red"
        
        label_feedback.config(text=f"Senha gerada. Força: {forca_senha}", fg=cor)

    except ValueError:
        exibir_senha.delete(0, tk.END)
        exibir_senha.insert(0, "Erro: Tamanho inválido!")
        label_feedback.config(text="Erro: Tamanho inválido!", fg="red")

def salvar_senha_gui(entrada_plataforma, exibir_senha, label_feedback):
    """
    Função chamada pelo botão para salvar a senha.
    """
    plataforma = entrada_plataforma.get()
    senha_gerada = exibir_senha.get()
    if plataforma and senha_gerada:
        mensagem = salvar_senha(plataforma, senha_gerada)
        if mensagem.startswith("Erro"):
            label_feedback.config(text=mensagem, fg="red")
        else:
            label_feedback.config(text=mensagem, fg="green")
    else:
        label_feedback.config(text="Erro: Preencha a plataforma e gere a senha!", fg="red")

def copiar_senha_gui(exibir_senha, label_feedback):
    """
    Copia a senha exibida no campo de resultado para a área de transferência.
    """
    senha = exibir_senha.get()
    if senha and not senha.startswith("Erro:"):
        exibir_senha.clipboard_clear()
        exibir_senha.clipboard_append(senha)
        label_feedback.config(text="Senha copiada para a área de transferência!", fg="blue")
    elif senha.startswith("Erro:"):
        label_feedback.config(text="Não é possível copiar. Gere uma senha válida primeiro!", fg="red")
    else:
        label_feedback.config(text="Nenhuma senha para copiar.", fg="red")

def verificar_forca_senha(senha):
    """
    Verifica a força de uma senha com base em critérios de composição.
    Retorna uma pontuação de 0 a 6.
    """
    pontuacao = 0
    tamanho_senha = len(senha)

    # Critérios de composição
    tem_maiuscula = any(c.isupper() for c in senha)
    tem_minuscula = any(c.islower() for c in senha)
    tem_numero = any(c.isdigit() for c in senha)
    tem_especial = any(not c.isalnum() for c in senha)

    # Adiciona pontos por tipo de caractere
    if tem_maiuscula:
        pontuacao += 1
    if tem_minuscula:
        pontuacao += 1
    if tem_numero:
        pontuacao += 1
    if tem_especial:
        pontuacao += 1
    
    # Adiciona pontos por tamanho
    if tamanho_senha >= 8:
        pontuacao += 1
    if tamanho_senha >= 12:
        pontuacao += 1
    if tamanho_senha >= 16:
        pontuacao += 1
    
    # Traduz a pontuação para um status de força
    if pontuacao <= 2:
        return "Fraca"
    elif pontuacao <= 4:
        return "Média"
    else:
        return "Forte"
    
def validar_senha_em_tempo_real(event, entrada_validar, label_feedback_validar):
    senha = entrada_validar.get()
    if not senha:
        label_feedback_validar.config(text="", fg="black")
        return
        
    forca_senha = verificar_forca_senha(senha)

    if forca_senha == "Forte":
        cor = "green"
    elif forca_senha == "Média":
        cor = "orange"
    else:
        cor = "red"
        
    label_feedback_validar.config(text=f"Força: {forca_senha}", fg=cor)


def criar_gui():
    root = tk.Tk()
    root.title("Gerador de Senhas")
    root.geometry("500x600")

    # Define uma cor de fundo sólida para a janela
    root.config(bg="#f0f0f0") 

    # 1. Campo para o nome da plataforma
    label_plataforma = tk.Label(root, text="Plataforma:")
    label_plataforma.pack(pady=5)
    entrada_plataforma = tk.Entry(root, width=30)
    entrada_plataforma.pack(pady=5)

    # 2. Campo para o tamanho da senha
    label_tamanho = tk.Label(root, text="Quantidade de caracteres:")
    label_tamanho.pack(pady=5)
    entrada_tamanho = tk.Entry(root, width=10)
    entrada_tamanho.pack(pady=5)

    # 3. Caixa para os tipos de caracteres
    frame_caracteres = tk.LabelFrame(root, text="Tipo de Caracteres")
    frame_caracteres.pack(pady=10, padx=10)
    
    var_maiusculas = tk.BooleanVar(value=True)
    check_maiusculas = tk.Checkbutton(frame_caracteres, text="Maiúsculas", variable=var_maiusculas)
    check_maiusculas.pack(side="left", padx=10)

    var_minusculas = tk.BooleanVar(value=True)
    check_minusculas = tk.Checkbutton(frame_caracteres, text="Minúsculas", variable=var_minusculas)
    check_minusculas.pack(side="left", padx=10)

    var_numeros = tk.BooleanVar(value=True)
    check_numeros = tk.Checkbutton(frame_caracteres, text="Números", variable=var_numeros)
    check_numeros.pack(side="left", padx=10)

    var_especiais = tk.BooleanVar(value=True)
    check_especiais = tk.Checkbutton(frame_caracteres, text="Especiais", variable=var_especiais)
    check_especiais.pack(side="left", padx=10)

    # 4. Campo para opção de embaralhar
    var_embaralhar = tk.BooleanVar(value=True)
    check_embaralhar = tk.Checkbutton(root, text="Embaralhar Senha", variable=var_embaralhar)
    check_embaralhar.pack(pady=5)

    # Criação dos widgets que precisam de referência antecipada
    exibir_senha = tk.Entry(root, width=40)
    label_feedback = tk.Label(root, text="", fg="blue")
    
    # 5. Botão Gerar Senha
    botao_gerar = tk.Button(root, text="Gerar Senha", 
                            command=lambda: gerar_senha_gui(entrada_tamanho, var_maiusculas, var_minusculas,
                                                            var_numeros, var_especiais, var_embaralhar,
                                                            exibir_senha, label_feedback))
    botao_gerar.pack(pady=5)

    # 6. Campo para exibir a senha gerada
    label_resultado = tk.Label(root, text="Senha Gerada:")
    label_resultado.pack(pady=5)
    exibir_senha.pack(pady=5)

    # 7. Botões de ação adicionais
    frame_botoes_acao = tk.Frame(root)
    frame_botoes_acao.pack(pady=10)

    botao_salvar = tk.Button(frame_botoes_acao, text="Salvar Senha",
                             command=lambda: salvar_senha_gui(entrada_plataforma, exibir_senha, label_feedback))
    botao_salvar.pack(side="left", padx=5)

    botao_copiar = tk.Button(frame_botoes_acao, text="Copiar Senha",
                             command=lambda: copiar_senha_gui(exibir_senha, label_feedback))
    botao_copiar.pack(side="left", padx=5)

    # 8. Rótulo de status
    label_feedback.pack(pady=10)

    # 9. Frame para validar a força de uma senha manualmente
    frame_validador = tk.LabelFrame(root, text="Validar Força da Senha")
    frame_validador.pack(pady=20, padx=10, fill="x")

    label_validar = tk.Label(frame_validador, text="Digite a senha:")
    label_validar.pack(pady=5)

    entrada_validar = tk.Entry(frame_validador, width=40)
    entrada_validar.bind("<KeyRelease>", lambda event: validar_senha_em_tempo_real(event, entrada_validar, label_feedback_validar))
    entrada_validar.pack(pady=5)
    
    label_feedback_validar = tk.Label(frame_validador, text="", fg="blue")
    label_feedback_validar.pack(pady=5)
    
    root.mainloop()

if __name__ == "__main__":
    criar_gui()
