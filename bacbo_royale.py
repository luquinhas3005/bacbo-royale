
import streamlit as st
import pandas as pd
import random
import time
import plotly.express as px
from datetime import datetime
import json
import os

st.set_page_config(page_title="Bac Bo Royale", layout="centered")

# Caminho de gravação local
ARQUIVO_HISTORICO = "historico_bacbo.json"

# 🎨 Tema claro/escuro
modo_escuro = st.sidebar.checkbox("🌙 Modo Escuro", value=True)
cor_fundo = "#111" if modo_escuro else "#fafafa"
cor_texto = "gold" if modo_escuro else "#333"

st.markdown(f"<h2 style='text-align: center; color: {cor_texto};'>🎰 Bac Bo Royale 🎰</h2>", unsafe_allow_html=True)
st.markdown(f"<div style='background-color: {cor_fundo}; padding: 20px; border-radius: 15px;'>", unsafe_allow_html=True)

# 🔄 Carregar histórico salvo
if "historico" not in st.session_state:
    if os.path.exists(ARQUIVO_HISTORICO):
        with open(ARQUIVO_HISTORICO, "r") as f:
            st.session_state.historico = json.load(f)
    else:
        st.session_state.historico = []

# 🎲 Simulação de rodada
def simular_rodada():
    st.markdown("""
        <audio autoplay>
            <source src="https://www.myinstants.com/media/sounds/dice-roll.mp3" type="audio/mpeg">
        </audio>
    """, unsafe_allow_html=True)

    st.image("https://media.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif", caption="🎲 Dados rolando...")
    time.sleep(1.5)

    dados = {
        "Data/Hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Player 1": random.randint(1, 6),
        "Player 2": random.randint(1, 6),
        "Banker 1": random.randint(1, 6),
        "Banker 2": random.randint(1, 6),
    }
    player_total = dados["Player 1"] + dados["Player 2"]
    banker_total = dados["Banker 1"] + dados["Banker 2"]

    if player_total > banker_total:
        resultado = "🧍 Player"
    elif banker_total > player_total:
        resultado = "🏦 Banker"
    else:
        resultado = "⚖️ Tie"

    dados["Resultado"] = resultado
    st.session_state.historico.append(dados)

    # 💾 Salvar após cada rodada
    with open(ARQUIVO_HISTORICO, "w") as f:
        json.dump(st.session_state.historico, f)

# ▶️ Botão de rolagem
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
if st.button("🎰 Rodar Dados", use_container_width=True):
    simular_rodada()

# 📋 Mostrar histórico
if st.session_state.historico:
    df = pd.DataFrame(st.session_state.historico)
    df["Player Total"] = df["Player 1"] + df["Player 2"]
    df["Banker Total"] = df["Banker 1"] + df["Banker 2"]

    st.markdown(f"<h4 style='color: {cor_texto};'>📊 Histórico de Rodadas</h4>", unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)

    # 📁 Botão para exportar CSV
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Baixar Histórico CSV", csv, "historico_bacbo.csv", "text/csv")

    # ⚠️ Alertas de padrões
    ultimos = df["Resultado"].tail(3).tolist()
    if len(ultimos) == 3 and all(x == "🧍 Player" for x in ultimos):
        st.warning("⚠️ Player venceu 3 vezes seguidas!")
    elif len(ultimos) == 3 and all(x == "🏦 Banker" for x in ultimos):
        st.warning("⚠️ Banker venceu 3 vezes seguidas!")
    elif len(ultimos) == 3 and all(x == "⚖️ Tie" for x in ultimos):
        st.warning("⚠️ Empate 3 vezes seguidas!")

    # 📊 Gráficos
    contagem = df["Resultado"].value_counts()
    st.markdown(f"<h4 style='color: {cor_texto};'>📈 Frequência de Resultados</h4>", unsafe_allow_html=True)
    st.bar_chart(contagem)

    st.markdown(f"<h4 style='color: {cor_texto};'>🧁 Distribuição</h4>", unsafe_allow_html=True)
    fig = px.pie(
        names=contagem.index,
        values=contagem.values,
        color_discrete_sequence=["#FFD700", "#FF4136", "#2ECC40"]
    )
    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Clique no botão acima para iniciar a simulação.")

st.markdown("</div>", unsafe_allow_html=True)
