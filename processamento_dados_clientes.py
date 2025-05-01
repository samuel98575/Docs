'''
Autor: Samuel Origa da Silva
Data de criação: 29/04/2025
Versão: 1.0

Script: processamento_dados_clientes.py
Descrição:
Este script realiza a leitura, análise e manipulação de dados de clientes a partir de um arquivo CSV.
Inclui tratamento de dados ausentes, conversão de tipos, criação de colunas derivadas (como localização e faixa etária),
identificação de outliers, manipulação de datas e exportação de resultados para novos arquivos.

Funcionalidades:
- Leitura de arquivos CSV com estrutura tabular de clientes.
- Visualização e exploração inicial dos dados.
- Tratamento de valores nulos e duplicados.
- Criação de colunas derivadas: Localização, Faixa Etária, Data formatada.
- Filtros por idade e condições múltiplas (ex: cidade + faixa etária).
- Agrupamento e cálculo de média por categorias (ex: por sexo).
- Detecção e remoção de outliers com Z-Score.
- Ordenação, renomeação e remoção de colunas.
- Conversão de tipos (int, str, datetime).
- Manipulação de datas (extração de ano, mês, dia e nome do dia).
- Exportação do DataFrame final em formato CSV.

Requisitos:
- Python 3.11.9
- Bibliotecas: pandas, scipy, os

Uso:
Execute o script em um ambiente com as bibliotecas instaladas e garanta que o arquivo de entrada esteja no caminho correto.
'''



# Importar a biblioteca Pandas
import pandas as p; # Nomear para facilitar no desenvolvimento

# Mapeamente do endereço do arquivo
arquivo = (f"Dados\dados.csv.txt");

# Ler CSV e gerar estrutura de dataframe
dataframe = p.read_csv(arquivo, sep=",");

# Visualizar os 10 primeiros registros
print("\nVisualizar os 10 primeiros registros do dataframe:");
print(dataframe.head(10));

# Explorar os dados:
print("\nInformação dos dados:");
dataframe.info(); # Informações dos dados
print("\nEstatística descritiva dos dados:");
print(dataframe.describe())  # Estatísticas descritivas dos dados quantitativos (idade)
dataframe.isnull()                  # Verifica valores nulos (True/False)
dataframe.isnull().sum()            # Conta quantos valores nulos por coluna
dataframe.dropna()                  # Remove linhas com valores nulos
dataframe.fillna("Desconhecido")   # Preenche valores nulos com texto




# Criar novas colunas através das colunas existentes
dataframe["Localização"] = dataframe["Bairro"] + ", " + dataframe["Cidade"];


# Agrupamento pegando a média de idade por sexo:
print("\nAgrupamento por sexo: ");
grupo_por_sexo = dataframe.groupby("Sexo")["Idade"].mean();
print(grupo_por_sexo);

# Realizar Filtro por idade
print("\nFiltro por idade superior o 30 anos: ");
dataframeFiltrado = dataframe[dataframe["Idade"] > 30];
print(dataframeFiltrado.head());

# Realizar filtros com multiplas condições:
print("\nFiltro por idade superior o 30 anos e cidade é São Paulo: ");
filtro = (dataframe["Idade"] > 30) & (dataframe["Cidade"] == "São Paulo");
df_filtrado = dataframe[filtro];
print(df_filtrado);


# Realizar ordenação dos dados por idade (Crescente):
print("\nRealizar ordenação dos dados por idade (Crescente): ");
dataframe_ordenado = dataframe.sort_values(by="Idade", ascending=True);
print(dataframe_ordenado);


# Remover colunas do dataframe:
print("\nRemover colunas do dataframe:: ");
dataframe_sem_cidade = dataframe.drop(columns=["Cidade"]);
print(dataframe_sem_cidade.head());

# Renomear colunas
print("\nRenomear colunas do dataframe: ");
dataframe_renomeado = dataframe.rename(columns={"Nome": "Primeiro Nome", "Idade": "Anos"});
print(dataframe_renomeado);

# Função para calcular a faixa etária
def faixa_etaria(idade):
    if idade < 18:
        return "Menor de idade";
    elif idade < 30:
        return "Jovem";
    else:
        return "Adulto";

dataframe["Faixa Etária"] = dataframe["Idade"].apply(faixa_etaria);

print(dataframe);


# Usando o Z-Score para detectar outliers
from scipy.stats import zscore
dataframe["Z-Score"] = zscore(dataframe["Idade"])
dataframe_sem_outliers = dataframe[dataframe["Z-Score"].abs() < 3]

# Modificar valores:
dataframe["Sexo"].replace({"M": "Masculino", "F": "Feminino"}, inplace=True)


# Realizar conversão de dados:
dataframe["Idade"] = dataframe["Idade"].astype(str)  # Converte para string
dataframe["Data"] = p.to_datetime(dataframe["Data"], infer_datetime_format=True, errors="coerce") # Converte para data
print(dataframe.info());

# Trabalhando com datas:
dataframe["Ano"] = dataframe["Data"].dt.year;
dataframe["Mês"] = dataframe["Data"].dt.month;
dataframe["Dia"] = dataframe["Data"].dt.day;
dataframe["Dia da Semana"] = dataframe["Data"].dt.day_name();
print("\nDataframe com novas colunas de data: ");
print(dataframe);

# Remover duplicatas
'''
dataframe.drop_duplicates(inplace=True);
'''

# Salvar um dataframe em arquivo CSV:
dataframe_renomeado.to_csv(f"Dados\clientesRenomeado.csv", index=False);





