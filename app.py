import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects

# Configurar o layout da página
st.set_page_config(layout="wide")
# Lê o arquivo csv
df = pd.read_csv('houses_to_rent_v2.csv')
# Criar um título para o dashboard
st.markdown("<h1 style='color:lightskyblue'>Dashboard de Casas para alugar</h1>", unsafe_allow_html=True)
# Criar um título para a barra lateral
st.sidebar.title("Filtros")
# Criar uma caixa (multiselect) pra selecionar as cidades
city_filter = st.sidebar.multiselect(
    "Selecione a(s) cidade(s)", options=df['city'].unique(), default=df['city'].unique()
)
# Aplicar filtros
filtered_df = df[df['city'].isin(city_filter)]
# Criar um botão para exibir o dataframe filtrado pelo multiselect
filter_button = st.sidebar.button("Dados filtrados")
# Cria 2 colunas para exibir os gráficos
col1, col2 = st.columns(2)
# Coluna 1: Gráficos a serem exibidos na primeira coluna
with col1:
    # Gráfico 1: Pizza sobre casas que aceitam ou não animais
    st.subheader("Propriedades que Aceitam Animais")
    
    # Verificar se há dados na coluna 'animal'
    if 'animal' in filtered_df.columns:
        # Contagem dos valores únicos na coluna 'animal'
        animal_counts = filtered_df['animal'].value_counts()
        # Criar labels customizadas
        labels = ['Aceitos', 'Não Aceitos']
        # Criando o gráfico de pizza
        fig, ax = plt.subplots(figsize=(10, 7.2))
        ax.pie(animal_counts, labels=labels, autopct='%1.1f%%', colors=['steelblue', 'lightgray'], startangle=90)
        ax.axis('equal')  # Garantir que o gráfico seja um círculo
        
        # Mostrar o gráfico no Streamlit
        st.pyplot(fig)
    else:
        st.write("A coluna 'animal' não está presente no dataset.")
    
    # Gráfico 2: Área Média por Cidade
    st.subheader("Área Média por Cidade")

    # Verificar se a coluna 'area' está presente
    if 'area' in filtered_df.columns and 'city' in filtered_df.columns:
        # Agrupar por cidade e calcular a área média
        avg_area_by_city = filtered_df.groupby('city')['area'].mean()

        # Criando o gráfico de barras para a área média por cidade
        fig, ax = plt.subplots(figsize=(10, 6))
        avg_area_by_city.plot(kind='bar', ax=ax, color='navy')
        ax.set_xlabel("")
        ax.set_ylabel("Área Média (m²)")
        # Remover linha da direita e de cima
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        # Rotacionar os nomes das cidades no eixo x
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
        # Mostrar gráfico
        st.pyplot(fig)
    else:
        st.write("As colunas 'area' e 'city' não estão presentes no dataset.")
    
with col2:
    # Gráfico 3: Casas mobiliadas
    st.subheader("Casas Mobiliadas por Cidade")
    # Criar uma tabela de frequência entre as colunas 'city' e 'furniture'
    furniture_city = pd.crosstab(filtered_df['city'], filtered_df['furniture'])
    # Definir o tamanho da figura
    fig, ax = plt.subplots(figsize=(10, 6))
    # Criar o gráfico de barras agrupadas
    furniture_city.plot(kind='bar', ax=ax, color=['mediumslateblue', 'silver'], width=0.75)
    # Ajustar os rótulos
    ax.set_xlabel('')
    # Rotacionar os rótulos no eixo X para melhor leitura
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    # Remover o eixo Y
    ax.yaxis.set_visible(False)
    # Adicionar uma legenda personalizada
    ax.legend(['Mobiliados', 'Não Mobiliados'], title='Casas')
    # Remover as linhas de contorno
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # Adicionar os valores acima de cada barra
    for container in ax.containers:
        for bar in container:
            height = bar.get_height()
            ax.annotate(f'{height}',
                         xy=(bar.get_x() + bar.get_width() / 2, height),  # Coordenadas x e y
                         xytext=(0, 5),  # Deslocamento
                         textcoords="offset points",  # Sistema de coordenadas
                         ha='center', va='bottom')  # Alinhamento

    # Exibir o gráfico no Streamlit
    st.pyplot(fig)

    # Gráfico 4: Valor médio do Aluguel por cidade 
    st.subheader("Preço Médio de Aluguel por Cidade")
    fig, ax = plt.subplots()
    price_data = filtered_df.groupby('city')['rent amount (R$)'].mean().sort_values(ascending=False)
    sns.barplot(x=price_data.values, y=price_data.index, ax=ax)
    ax.set_xlabel("Aluguel Médio (R$)")
    ax.set_ylabel("")
    # Remover linha da direita e de cima
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    # Mostrar o gráfico
    st.pyplot(fig)

# Gráfico 5: Médias das Taxas por Cidade (HOA, Property Tax, Fire Insurance)
st.subheader(":rainbow[Médias das Taxas por Cidade]")
    
# Verificar se há dados suficientes para as colunas de taxas
if 'hoa (R$)' in filtered_df.columns and 'property tax (R$)' in filtered_df.columns and 'fire insurance (R$)' in filtered_df.columns:
    # Agrupar os dados por cidade e calcular a média das taxas
    avg_taxes_by_city = filtered_df.groupby('city')[['hoa (R$)', 'property tax (R$)', 'fire insurance (R$)']].mean()
    
    # Configurar gráfico de barras agrupadas
    fig, ax = plt.subplots(figsize=(10, 6))
    avg_taxes_by_city.plot(kind='bar', ax=ax, color=['steelblue', 'darkorange', 'red'], width=0.8)
    ax.set_xlabel("")
    ax.legend(["HOA", "Property Tax", "Fire Insurance"], title="Taxas")
        
    # Adicionar uma mensagem no gráfico
    message = 'Maior taxa de condomínio (HOA) é a de Belo\
    \nHorizonte. São Paulo, que tem um aluguel\
    \nmédio maior, possui um valor bem abaixo\
    \ndo que o de BH'
    ax.text(1, 2000, message, fontsize=10, color='midnightblue', 
                   bbox=dict(facecolor='white', edgecolor='lightgray', boxstyle='round,pad=0.5'))
    
    # Rotacionar os nomes das cidades no eixo x
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    # Remover o eixo Y
    ax.yaxis.set_visible(False)
    # Remover as linhas de contorno (spines)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # Adicionar os valores acima de cada barra
    for container in ax.containers:
        for bar in container:
            height = bar.get_height()
            ax.annotate(f'{height:.2f}',  # Formatar para duas casas decimais
                         xy=(bar.get_x() + bar.get_width() / 2, height),  # Coordenadas x e y
                         xytext=(0, 5),  # Deslocamento
                         textcoords="offset points",  # Sistema de coordenadas
                         ha='center', va='bottom')  # Alinhamento
    # Mostrar gráfico
    st.pyplot(fig)
else:
    st.write("As colunas 'hoa (R$)', 'property tax (R$)' e 'fire insurance (R$)' não estão presentes no dataset.")

if filter_button:
    # Exibindo o DataFrame filtrado
    st.write(":gray[Dados Filtrados]", filtered_df)







