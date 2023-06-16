import tkinter as tk
from tkinter import ttk, messagebox
from collections import Counter
import os
from matminer.datasets import load_dataset
import pandas as pd
import pickle


with open("dados.pickle", "rb") as arquivo:
    lista_dados_base = pickle.load(arquivo)


datasets_dicionario, datasets, todas_colunas, dataset_nome_colunas = lista_dados_base


def dataset_selecionado(event):
    dataset = escolha_datasets.get()
    if dataset == "Todos":
        colunas = todas_colunas
    else:
        descrição_dataset_text.configure(state="normal")
        descrição_dataset_text.delete("1.0", tk.END)
        descrição_dataset_text.insert(
            tk.END,
            "Nome do dataset:\n"
            + dataset
            + "\n\n"
            + "Descrição:\n"
            + datasets_dicionario[dataset]["descrição"],
        )
        descrição_dataset_text.configure(state="disabled")

        colunas = list(datasets_dicionario[dataset].keys())
        colunas.remove("descrição")

    choicesvar.set(colunas)  # type: ignore
    coluna_descricao_text.configure(state="normal")
    coluna_descricao_text.delete("1.0", tk.END)
    coluna_descricao_text.configure(state="disabled")


def item_selecionado(event):
    posicao = colunas_selecao.curselection()
    if posicao:
        if escolha_datasets.get() == "Todos":
            dataset = dataset_nome_colunas[posicao[0]]
            descrição_dataset_text.configure(state="normal")

            descrição_dataset_text.delete("1.0", tk.END)
            descrição_dataset_text.insert(
                tk.END,
                "Nome do dataset:\n"
                + dataset
                + "\n\n"
                + "Descrição:\n"
                + datasets_dicionario[dataset]["descrição"],
            )
            descrição_dataset_text.configure(state="disabled")

        else:
            dataset = escolha_datasets.get()

        coluna = colunas_selecao.get(posicao[0])
        coluna_descricao_text.configure(state="normal")
        coluna_descricao_text.delete("1.0", tk.END)
        coluna_descricao_text.insert(
            tk.END,
            "Nome da coluna:\n"
            + coluna
            + "\n\n"
            + "Descrição da coluna:\n"
            + datasets_dicionario[dataset][coluna],
        )
        coluna_descricao_text.configure(state="disabled")
        if (coluna, dataset) in lista_colunas_selecionadas:
            botao_remover.config(state="active")
            botao_adicionar.config(state="disabled")
        else:
            botao_adicionar.config(state="active")
            botao_remover.config(state="disabled")


def palavra_chave(event):
    coluna = []
    lista_palavras = entrada.get().split(" ")  # separa entrada em palavras
    dataset_escolhido = escolha_datasets.get()  # escolha de dataset do usuario
    if dataset_escolhido == "Todos":
        global dataset_nome_colunas  # chamar variavel global
        dataset_nome_colunas.clear()  # limpar nomes dos datasets para vincular novamente

        for entrada_chave in lista_palavras:  # cada palavra chave
            for (
                dataset_name,
                dataset,
            ) in datasets_dicionario.items():  # em cada dataset do dicionario
                for (
                    column_name,
                    column_description,
                ) in dataset.items():  # em cada coluna e descrição
                    if (
                        entrada_chave.lower() in column_description.lower()
                    ) or entrada_chave.lower() in column_name.lower():  # detecção da palavra
                        if (
                            column_name != "descrição"
                        ):  # colocar somente se ainda não existir e se n for "descrição"
                            coluna.append(column_name)  # add na lista coluna
                            dataset_nome_colunas.append(
                                dataset_name
                            )  # add nome dataset para vinculação
    else:
        for entrada_chave in lista_palavras:  # em cada palavra chave
            for column_name, column_description in datasets_dicionario[
                dataset_escolhido
            ].items():  # for somente no dataset escolido
                if (
                    entrada_chave.lower() in column_description.lower()
                    or entrada_chave.lower() in column_name.lower()
                ):  # detecção da palavra
                    if (
                        column_name not in coluna and column_name != "descrição"
                    ):  # colocar somente se ainda não existir e se n for "descrição"
                        coluna.append(column_name)
    if coluna == []:
        messagebox.showerror(
            "Erro", "Nenhuma correspondência com essa pesquisa."
        )  # se n tiver nenhuma correspondência da erro e n faz nada
    else:
        choicesvar.set(coluna)  # type: ignore # set as colunas correspondêntes


def adicionar_item():
    global lista_colunas_selecionadas
    posicao = colunas_selecao.curselection()
    if posicao:
        dataset = escolha_datasets.get()
        if dataset == "Todos":
            dataset = dataset_nome_colunas[posicao[0]]
        coluna = colunas_selecao.get(posicao[0])
        lista_colunas_selecionadas.append((coluna, dataset))
    botao_remover.config(state="active")
    botao_adicionar.config(state="disabled")


def remover_item():
    global lista_colunas_selecionadas
    posicao = colunas_selecao.curselection()
    if posicao:
        dataset = escolha_datasets.get()
        if dataset == "Todos":
            dataset = dataset_nome_colunas[posicao[0]]
        coluna = colunas_selecao.get(posicao[0])
        lista_colunas_selecionadas.remove((coluna, dataset))
    botao_remover.config(state="disabled")
    botao_adicionar.config(state="active")


def mostrar_selecionadas():
    global lista_colunas_selecionadas
    # Criar a janela de pop-up
    popup = tk.Toplevel(janela)
    popup.title("Lista de Seleção")
    popup.grab_set()

    explicação = tk.Text(popup, height=5, width=20, wrap=tk.WORD)
    explicação.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky=tk.NSEW)
    explicação.insert(
        tk.END,
        "O botão remover vai remover as colunas selecionadas, o botão criar vai criar um dataset com o nome dos datasets na primeira linha e o nome de cada coluna do mesmo nas colunas subsequentes.",
    )
    explicação.configure(state="disabled")

    # Criar a lista de seleção múltipla com checkboxes
    lista = tk.Listbox(popup, selectmode=tk.MULTIPLE)
    lista.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

    # Adicionar itens à lista
    for item in lista_colunas_selecionadas:
        linha = f"Coluna: {item[0]}, dataset: {item[1]}"
        lista.insert(tk.END, linha)

    lista.configure(width=50, height=10)

    def remover_pop_up():
        global lista_colunas_selecionadas
        lista_copia = lista_colunas_selecionadas.copy()
        selecao = lista.curselection()
        if selecao:
            # Exibir os itens selecionados
            for posicao in reversed(selecao):
                lista_colunas_selecionadas.remove(lista_copia[posicao])
                lista.delete(posicao)
            botao_remover_pop_up.config(state=tk.DISABLED)

    # Ideia para juntar dados
    # def juntar_dados():
    #     if lista_colunas_selecionadas != []:
    #         datasets = set(dado[1] for dado in lista_colunas_selecionadas)
    #         colunas_datasets = []
    #         colunas_dataset_total = []
    #         for dataset in datasets:
    #             colunas_datasets.append((get_dataset_columns(dataset), dataset))
    #             colunas_dataset_total += get_dataset_columns(dataset)
    #         # Obtém o item mais comum e sua contagem
    #         contador = Counter(colunas_dataset_total)
    #         coluna_mais_comum = contador.most_common(1)[0][0]
    #         print(coluna_mais_comum)
    #         dataset_faltantes = []
    #         for colunas_e_dataset in colunas_datasets:
    #             if coluna_mais_comum == "formula":
    #                 if (
    #                     coluna_mais_comum not in colunas_e_dataset[0]
    #                     and "composition" not in colunas_e_dataset[0]
    #                 ):
    #                     dataset_faltantes.append(colunas_e_dataset[1])
    #             elif coluna_mais_comum == "composition":
    #                 if (
    #                     coluna_mais_comum not in colunas_e_dataset[0]
    #                     and "formula" not in colunas_e_dataset[0]
    #                 ):
    #                     dataset_faltantes.append(colunas_e_dataset[1])
    #             else:
    #                 if coluna_mais_comum not in colunas_e_dataset[0]:
    #                     dataset_faltantes.append(colunas_e_dataset[1])

    #         if dataset_faltantes != []:
    #             messagebox.showerror(
    #                 "Erro",
    #                 f'Esses datasets {dataset_faltantes} não possuem a coluna "{coluna_mais_comum}", que é a coluna que mais aparece nos datastes selecionados, por equanto não tem solução, recomendamos remover da escolha as colunas destes datastes.',
    #             )
    #         else:
    #             criar = messagebox.askyesno(
    #                 "Dataset", "Certeza que deseja criar o dataset com essas colunas?"
    #             )
    #             if criar:
    #                 dados = importar_dados()
    #     else:
    #         messagebox.showerror("Erro", "Ainda não foi selecionado colunas.")

    def baixar():
        """Cria e exporta um dataset com os nomes do dataset na primeira coluna e as colunas de cada dataset colunas seguintes, dentro da mesma linha."""
        dicionario = {}
        for coluna_selecionada, dataset_selecionado in lista_colunas_selecionadas:
            try:
                dicionario[dataset_selecionado].append(coluna_selecionada)
            except:
                dicionario[dataset_selecionado] = []
                dicionario[dataset_selecionado].append(dataset_selecionado)
                dicionario[dataset_selecionado].append(coluna_selecionada)

        dataset_selecionado = pd.DataFrame.from_dict(dicionario, orient="index")
        dataset_selecionado.to_csv("Dados.csv", index=False)

    def on_select(event):
        # Verifica se há algum item selecionado
        if lista.curselection():
            # Habilita o botão de remoção se houver seleção
            botao_remover_pop_up.config(state=tk.NORMAL)
        else:
            # Desabilita o botão de remoção se não houver seleção
            botao_remover_pop_up.config(state=tk.DISABLED)

    botao_remover_pop_up = tk.Button(popup, text="Remover", command=remover_pop_up)
    botao_remover_pop_up.grid(row=2, column=0, padx=10, pady=10)
    botao_remover_pop_up.config(state=tk.DISABLED)

    botao_criar_pop_up = tk.Button(popup, text="Baixar", command=baixar)  # type: ignore
    botao_criar_pop_up.grid(row=2, column=1, padx=10, pady=10)

    botao_cancelar_pop_up = tk.Button(popup, text="Cancelar", command=popup.destroy)
    botao_cancelar_pop_up.grid(row=2, column=2, padx=10, pady=10)

    lista.bind("<<ListboxSelect>>", on_select)


lista_colunas_selecionadas = list()

janela = tk.Tk()
janela.title("Receber Palavra")

rotulo = tk.Label(janela, text="Escreva a palavra:")
rotulo.grid(row=0, column=0, padx=10, columnspan=2, pady=10, sticky="ew")

entrada = tk.Entry(janela)
entrada.grid(row=1, column=0, padx=10, pady=10)
entrada.bind("<Return>", palavra_chave)


datasets.insert(0, "Todos")
valor_padrao = tk.StringVar()
escolha_datasets = ttk.Combobox(
    janela, values=datasets, textvariable=valor_padrao, width=30
)
escolha_datasets.bind("<<ComboboxSelected>>", dataset_selecionado)
escolha_datasets.grid(row=2, column=0, padx=10, pady=10)
valor_padrao.set(datasets[0])

choicesvar = tk.StringVar(value=todas_colunas)  # type: ignore
colunas_selecao = tk.Listbox(janela, listvariable=choicesvar)
colunas_selecao.grid(row=3, column=0, padx=10, pady=10)
colunas_selecao.bind("<<ListboxSelect>>", item_selecionado)

mostrar_selecionadas_botao = tk.Button(
    janela, text="Mostrar\nadicionadas", command=mostrar_selecionadas
)
mostrar_selecionadas_botao.grid(row=4, column=0, padx=10, pady=10)


descrição_dataset_text = tk.Text(janela, height=5, width=20, wrap=tk.WORD)
descrição_dataset_text.grid(
    row=1, column=1, columnspan=2, rowspan=2, padx=10, pady=10, sticky=tk.NSEW
)
descrição_dataset_text.configure(state="disabled")

coluna_descricao_text = tk.Text(janela, height=3, width=20, wrap=tk.WORD)
coluna_descricao_text.grid(
    row=3, columnspan=2, column=1, padx=10, pady=10, sticky=tk.NSEW
)
coluna_descricao_text.configure(state="disabled")


botao_adicionar = tk.Button(janela, text="Adicionar", command=adicionar_item)
botao_adicionar.grid(row=4, column=1, padx=10, pady=10)


botao_remover = tk.Button(janela, text="Remover", command=remover_item)
botao_remover.grid(row=4, column=2, padx=10, pady=10)

botao_adicionar.config(state="disabled")
botao_remover.config(state="disabled")

janela.mainloop()
