import streamlit as st
import pandas as pd
import os
from datetime import date

# --- Configurações e Funções Auxiliares ---
CSV_FILE = 'competicoes.csv'

def load_data():
    """Carrega os dados das competições."""
    if not os.path.exists(CSV_FILE):
        return pd.DataFrame(columns=['ID', 'Competicao', 'Temporada', 'DataFinal', 'Campeao'])
    
    # Garante que a coluna de data seja interpretada corretamente
    df = pd.read_csv(CSV_FILE, parse_dates=['DataFinal'])
    return df

def save_data(df):
    """Salva o DataFrame de volta no CSV."""
    df.to_csv(CSV_FILE, index=False)

st.set_page_config(page_title="Fantasy - Competição Vigente", page_icon="🏆")

st.title("🔥 Competição Vigente")
st.write("Acompanhe aqui a competição que está mais perto da grande final!")

df = load_data()

# Filtra apenas as competições que ainda não têm um campeão definido
df_vigentes = df[pd.isna(df['Campeao'])].copy()

if df_vigentes.empty:
    st.info("Nenhuma competição em andamento. Cadastre uma nova na página 'Cadastrar Competição'!")
else:
    # Ordena para pegar a competição com a data final mais próxima
    df_vigentes = df_vigentes.sort_values(by='DataFinal', ascending=True)
    competicao_atual = df_vigentes.iloc[0]
    
    st.subheader(f"{competicao_atual['Competicao']} - {competicao_atual['Temporada']}")
    
    col1, col2 = st.columns(2)
    col1.metric("Data da Final", competicao_atual['DataFinal'].strftime('%d/%m/%Y'))
    
    hoje = pd.to_datetime(date.today())
    delta = competicao_atual['DataFinal'] - hoje
    
    col2.metric("Contagem Regressiva", f"{delta.days} dias")

    # --- LÓGICA PRINCIPAL: Mostrar formulário na data da final ---
    if hoje >= competicao_atual['DataFinal']:
        st.warning("A data final chegou! É hora de definir o campeão.", icon="🚨")
        
        with st.form("form_definir_campeao"):
            nome_campeao = st.text_input("👑 E o grande campeão é...")
            submitted = st.form_submit_button("Declarar Campeão!")
            
            if submitted:
                if not nome_campeao:
                    st.error("Você precisa informar o nome do campeão!")
                else:
                    # Encontra o índice da competição no DataFrame original para atualizar
                    index_para_atualizar = df[df['ID'] == competicao_atual['ID']].index
                    
                    # Atualiza o DataFrame original
                    df.loc[index_para_atualizar, 'Campeao'] = nome_campeao
                    
                    save_data(df)
                    st.balloons()
                    st.success(f"Parabéns a {nome_campeao}, campeão de {competicao_atual['Competicao']} {competicao_atual['Temporada']}!")
                    st.info("A página será recarregada para mostrar a próxima competição.")
                    st.rerun() # Recarrega a página
    else:
        st.info("Aguardando a data da final para a definição do campeão.")