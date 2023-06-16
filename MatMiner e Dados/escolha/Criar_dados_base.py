"""Vai ser utilizada unicamente para criar e traduzir os dados bases e depois enviar para um arquivo pickle."""
import pickle
from deep_translator import GoogleTranslator

linguas = GoogleTranslator(source="en", target="pt")

from matminer.datasets import (
    get_available_datasets,
    get_dataset_column_description,
    get_dataset_columns,
    get_dataset_description,
)

def dados_base():
    datasets_dicionario = {}
    datasets = get_available_datasets(
        print_format=None  # type: ignore
    )  # mostra os datasets disponiveis

    todas_colunas = []
    dataset_nome_colunas = []
    for dataset in datasets:
        datasets_dicionario[dataset] = {"descrição": linguas.translate(get_dataset_description(dataset))}
        colunas_dataset = get_dataset_columns(dataset)
        for coluna in colunas_dataset:
            todas_colunas.append(coluna)
            dataset_nome_colunas.append(dataset)
            descrição = linguas.translate(get_dataset_column_description(dataset, coluna))

            datasets_dicionario[dataset][coluna] = descrição
    return [datasets_dicionario, datasets, todas_colunas, dataset_nome_colunas]

nome_arquivo = "dados.pickle"
with open(nome_arquivo, 'wb') as arquivo:
    pickle.dump(dados_base(), arquivo)