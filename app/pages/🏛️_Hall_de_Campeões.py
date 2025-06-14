import streamlit as st
import pandas as pd
import os

# --- Configurações e Funções Auxiliares ---
CSV_FILE = 'competicoes.csv'

def load_data():
    """Carrega os dados das competições."""
    if not os.path.exists(CSV_FILE):
        return pd.DataFrame(columns=['ID', 'Competicao', 'Temporada', 'DataFinal', 'Campeao'])
    
    df = pd.read_csv(CSV_FILE, parse_dates=['DataFinal'])
    return df

st.set_page_config(page_title="Hall de Campeões", page_icon="🏛️")
st.title("🏛️ Hall de Campeões")
st.write("A lista imortal dos maiores managers da história da liga.")

df = load_data()

# Filtra apenas competições que JÁ TÊM um campeão
df_campeoes = df.dropna(subset=['Campeao'])

if df_campeoes.empty:
    st.info("Ainda não temos campeões registrados na história.")
else:
    # Exibe a tabela de campeões
    st.dataframe(
        df_campeoes[['Temporada', 'Competicao', 'Campeao']].sort_values(by='Temporada', ascending=False),
        hide_index=True,
        use_container_width=True
    )

    # Adiciona um pequeno gráfico de estatísticas
    st.divider()
    st.header("🏆 Maiores Vencedores")
    
    # Conta quantas vezes cada nome aparece na coluna 'Campeao'
    contagem_titulos = df_campeoes['Campeao'].value_counts()
    
    st.bar_chart(contagem_titulos)