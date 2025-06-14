import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Hall de Campeões", page_icon="🏛️")
st.title("🏛️ Hall de Campeões")
st.write("A lista imortal dos maiores managers da história da liga.")

# --- Conexão e Carregamento dos Dados ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(worksheet="Página1", usecols=list(range(5)), ttl="10m")
    df = df.dropna(how='all')
except Exception as e:
    st.error(f"Ocorreu um erro ao conectar ou ler a planilha. Verifique suas configurações. Erro: {e}")
    st.stop()

# --- Processamento e Lógica da Página ---

# Preenche valores vazios e garante que o campeão seja texto
df['Campeao'] = df['Campeao'].fillna('')
# Filtra apenas competições que JÁ TÊM um campeão (não são uma string vazia)
df_campeoes = df[df['Campeao'] != ''].copy()


if df_campeoes.empty:
    st.info("Ainda não temos campeões registrados na história.")
else:
    # Garante que a Temporada seja tratada como texto para exibição
    df_campeoes['Temporada'] = df_campeoes['Temporada'].astype(str)

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