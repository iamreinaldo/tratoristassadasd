import streamlit as st
import pandas as pd
from streamlit_gsheets.gsheets_connection import GSheetsConnection
from datetime import date

st.set_page_config(page_title="Cadastrar Competição", page_icon="➕")

st.title("➕ Cadastrar Nova Competição")
st.write("Use o formulário abaixo para registrar uma nova competição na liga.")

# --- Conexão com Google Sheets ---
# O Streamlit usa o `type=GSheetsConnection` para saber como usar as credenciais
# que você já configurou nos Secrets.
try:
    conn = st.connection("gsheets", type=GSheetsConnection)

    # Leitura dos dados da planilha
    df = conn.read(worksheet="Página1", usecols=list(range(5)), ttl="10m")
    # Filtra as linhas que possam estar completamente vazias
    df = df.dropna(how='all')

except Exception as e:
    st.error(f"Ocorreu um erro ao conectar ou ler a planilha. Verifique suas configurações. Erro: {e}")
    st.stop()


# --- Formulário ---
with st.form("form_nova_competicao", clear_on_submit=True):
    competicao = st.text_input("Nome da Competição (Ex: Brasileirão, Copa do Mundo)")
    temporada = st.text_input("Temporada (Ex: 2025)")
    data_final = st.date_input("Data da Final", min_value=date.today())
    
    submitted = st.form_submit_button("Cadastrar")

    if submitted:
        if not competicao or not temporada:
            st.warning("Por favor, preencha o nome da competição e a temporada.")
        else:
            # Garante que a coluna ID seja numérica para encontrar o máximo
            df['ID'] = pd.to_numeric(df['ID'], errors='coerce')
            novo_id = (df['ID'].max() + 1) if not df.empty else 1
            
            # Cria um novo DataFrame para a nova linha
            nova_competicao_df = pd.DataFrame([{
                'ID': novo_id,
                'Competicao': competicao,
                'Temporada': temporada,
                'DataFinal': data_final.strftime("%Y-%m-%d"), # Salva a data como texto
                'Campeao': '' # Deixa o campeão em branco
            }])
            
            # Adiciona os novos dados ao DataFrame existente
            df_atualizado = pd.concat([df, nova_competicao_df], ignore_index=True)
            
            # Atualiza a planilha inteira com os novos dados
            # O método .update() do conector substitui os dados existentes pelos do DataFrame.
            conn.update(worksheet="Página1", data=df_atualizado)
            
            st.success(f"Competição '{competicao} {temporada}' cadastrada com sucesso!")