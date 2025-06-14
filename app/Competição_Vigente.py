import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import date

st.set_page_config(page_title="Fantasy - Competição Vigente", page_icon="🏆")

st.title("🔥 Competição Vigente")
st.write("Acompanhe aqui a competição que está mais perto da grande final!")

# --- Conexão e Carregamento dos Dados ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(worksheet="Página1", usecols=list(range(5)), ttl="10m")
    df = df.dropna(how='all')
except Exception as e:
    st.error(f"Ocorreu um erro ao conectar ou ler a planilha. Verifique suas configurações. Erro: {e}")
    st.stop()

# --- Processamento e Lógica da Página ---

# Converte colunas para os tipos corretos
df['ID'] = pd.to_numeric(df['ID'])
df['DataFinal'] = pd.to_datetime(df['DataFinal'])
# Preenche valores vazios na coluna campeão para garantir a filtragem correta
df['Campeao'] = df['Campeao'].fillna('')

# Filtra apenas as competições que ainda não têm um campeão definido
df_vigentes = df[df['Campeao'] == ''].copy()

if df_vigentes.empty:
    st.info("🎉 Todas as competições foram finalizadas! Cadastre uma nova na página 'Cadastrar Competição'!")
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
                    # Altera o valor 'Campeao' no DataFrame original para a competição atual
                    df.loc[df['ID'] == competicao_atual['ID'], 'Campeao'] = nome_campeao
                    
                    # Salva o DataFrame inteiro de volta na planilha
                    conn.update(worksheet="Página1", data=df)
                    
                    st.balloons()
                    st.success(f"Parabéns a {nome_campeao}, campeão de {competicao_atual['Competicao']} {competicao_atual['Temporada']}!")
                    st.rerun() # Recarrega a página para atualizar as informações
    else:
        st.info("Aguardando a data da final para a definição do campeão.")