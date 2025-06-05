
import streamlit as st
import random
import base64
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Bac Bo Royale", layout="centered", page_icon="🎲")

# Tema escuro/claro
st.markdown("""
<style>
body {
    color: #f0f0f0;
    background-color: #0e1117;
}
[data-theme="light"] body {
    background-color: #ffffff;
    color: #000000;
}
</style>
""", unsafe_allow_html=True)

st.title("🎲 Bac Bo Royale - Simulador Avançado")

# Inicializar estados
if "history" not in st.session_state:
    st.session_state.history = []

if "trigger_roll" not in st.session_state:
    st.session_state.trigger_roll = False

# Função para jogar
def rolar_dados():
    d1, d2 = random.randint(1, 6), random.randint(1, 6)
    d3, d4 = random.randint(1, 6), random.randint(1, 6)
    sum_a, sum_b = d1 + d2, d3 + d4
    result = "Empate"
    if sum_a > sum_b:
        result = "Player A"
    elif sum_b > sum_a:
        result = "Player B"

    st.session_state.history.append({
        "Player A": sum_a,
        "Player B": sum_b,
        "Resultado": result,
        "Data/Hora": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    })

# Botão de rolar dados
if st.button("🎲 Rolar Dados"):
    rolar_dados()

# Exibir histórico
if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)
    st.subheader("📜 Histórico de Resultados")
    st.dataframe(df[::-1], use_container_width=True)

    st.subheader("📊 Estatísticas")
    total = len(df)
    counts = df["Resultado"].value_counts()
    for res in ["Player A", "Player B", "Empate"]:
        count = counts.get(res, 0)
        st.write(f"**{res}**: {count} ({(count/total*100):.1f}%)")

    fig = px.bar(x=counts.index, y=counts.values, labels={"x": "Resultado", "y": "Frequência"})
    st.plotly_chart(fig, use_container_width=True)

    st.download_button("📁 Exportar CSV", df.to_csv(index=False).encode(), "historico_bacbo.csv", "text/csv")

    if st.button("🗑️ Resetar Histórico"):
        st.session_state.history = []

else:
    st.info("Clique em 'Rolar Dados' para iniciar.")
