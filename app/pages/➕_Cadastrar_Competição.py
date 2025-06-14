import streamlit as st
import pandas as pd
import os
from datetime import date

# --- Configurações e Funções Auxiliares ---
CSV_FILE = 'competicoes.csv'

def load_data():
    """Carrega os dados das competições, criando o arquivo se não existir."""
    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(columns=['ID', 'Competicao', 'Temporada', 'DataFinal', 'Campeao'])
        df.to_csv(CSV_FILE, index=False)
    
    # É crucial converter a coluna de data ao carregar
    df = pd.read_csv(CSV_FILE, parse_dates=['DataFinal'])
    return df

st.set_page_config(page_title="Cadastrar Competição", page_icon="➕")

st.title("➕ Cadastrar Nova Competição")
st.write("Use o formulário abaixo para registrar uma nova competição na liga.")

# --- Formulário ---
df = load_data()

with st.form("form_nova_competicao", clear_on_submit=True):
    competicao = st.text_input("Nome da Competição: ")
    temporada = st.text_input("Temporada (Ex: 2025 ou 25/26)")
    data_final = st.date_input("Data da Final", min_value=date.today())
    
    submitted = st.form_submit_button("Cadastrar")

    if submitted:
        if not competicao or not temporada:
            st.warning("Por favor, preencha o nome da competição e a temporada.")
        else:
            # Pega o último ID e soma 1 para o novo. Se não houver, começa com 1.
            novo_id = (df['ID'].max() + 1) if not df.empty else 1
            
            nova_competicao = pd.DataFrame([{
                'ID': novo_id,
                'Competicao': competicao,
                'Temporada': temporada,
                'DataFinal': pd.to_datetime(data_final),
                'Campeao': None # Começa sem campeão definido
            }])
            
            df_atualizado = pd.concat([df, nova_competicao], ignore_index=True)
            df_atualizado.to_csv(CSV_FILE, index=False)
            
            st.success(f"Competição '{competicao} {temporada}' cadastrada com sucesso!")