
import streamlit as st
import random
import pandas as pd
import plotly.express as px
import os
from pathlib import Path

st.set_page_config(page_title="Bac Bo Royale", layout="centered", page_icon="🎲")
HIST_FILE = "historico_bacbo.csv"

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

st.title("🎲 Bac Bo Royale - Animações & Sons")

# Sons e GIFs
def play_sound(file):
    st.markdown(f"""
    <audio autoplay>
        <source src="data:audio/wav;base64,{file}" type="audio/wav">
    </audio>
    """, unsafe_allow_html=True)

def load_base64(file_path):
    import base64
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

sound_win = load_base64("sounds/win.wav")
sound_lose = load_base64("sounds/lose.wav")
sound_draw = load_base64("sounds/draw.wav")
gif_path = "images/rolling.gif"

# Carregar histórico salvo
if os.path.exists(HIST_FILE):
    df = pd.read_csv(HIST_FILE)
else:
    df = pd.DataFrame(columns=["Player A", "Player B", "Resultado", "Data/Hora"])

if "history_df" not in st.session_state:
    st.session_state.history_df = df

# Função para jogar
def rolar_dados():
    d1, d2 = random.randint(1, 6), random.randint(1, 6)
    d3, d4 = random.randint(1, 6), random.randint(1, 6)
    sum_a, sum_b = d1 + d2, d3 + d4
    result = "Empate"
    sound = sound_draw
    if sum_a > sum_b:
        result = "Player A"
        sound = sound_win
    elif sum_b > sum_a:
        result = "Player B"
        sound = sound_lose

    new_row = {
        "Player A": sum_a,
        "Player B": sum_b,
        "Resultado": result,
        "Data/Hora": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state.history_df = pd.concat([st.session_state.history_df, pd.DataFrame([new_row])], ignore_index=True)
    st.session_state.history_df.to_csv(HIST_FILE, index=False)
    play_sound(sound)
    st.image(gif_path, width=300)

# Botão
if st.button("🎲 Rolar Dados"):
    rolar_dados()

# Histórico
df = st.session_state.history_df
if not df.empty:
    st.subheader("📜 Histórico")
    st.dataframe(df[::-1], use_container_width=True)

    st.subheader("📊 Estatísticas")
    total = len(df)
    counts = df["Resultado"].value_counts()
    for res in ["Player A", "Player B", "Empate"]:
        count = counts.get(res, 0)
        st.write(f"**{res}**: {count} ({(count/total*100):.1f}%)")
    st.plotly_chart(px.bar(x=counts.index, y=counts.values, labels={"x": "Resultado", "y": "Frequência"}), use_container_width=True)

    st.subheader("📈 Padrões")
    ultima = df["Resultado"].iloc[-1]
    seq = 1
    for i in range(len(df)-2, -1, -1):
        if df["Resultado"].iloc[i] == ultima:
            seq += 1
        else:
            break
    st.write(f"🔁 **Sequência atual**: {ultima} venceu {seq} vezes seguidas")

    freq = pd.concat([df["Player A"], df["Player B"]]).value_counts().sort_index()
    st.bar_chart(freq, use_container_width=True)
    st.write(f"🎯 **Média A**: {df['Player A'].mean():.2f} | **Média B**: {df['Player B'].mean():.2f}")

    st.download_button("📁 Exportar CSV", df.to_csv(index=False).encode(), "historico_bacbo.csv", "text/csv")

    if st.button("🗑️ Resetar Histórico"):
        st.session_state.history_df = pd.DataFrame(columns=["Player A", "Player B", "Resultado", "Data/Hora"])
        if os.path.exists(HIST_FILE):
            os.remove(HIST_FILE)
else:
    st.info("Clique em 'Rolar Dados' para começar.")
