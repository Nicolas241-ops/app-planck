import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Configurações globais da página web
st.set_page_config(page_title="Constante de Planck - Eletro", page_icon="💡", layout="centered")

# Constantes Físicas universais
c = 3e8       # Velocidade da luz (m/s)
e = 1.6e-19   # Carga do elétron (Coulombs)

st.title("💡 Análise de LEDs e Constante de Planck")
st.markdown("""
Este aplicativo calcula experimentalmente a **Constante de Planck ($h$)** utilizando as tensões de corte ($V_0$) 
e os comprimentos de onda ($\lambda$) de diferentes LEDs medidos em circuito.
""")

st.sidebar.header("🔧 Configurações do Experimento")

# Seleção da quantidade de LEDs por um slider na barra lateral
num_leds = st.sidebar.slider("Quantos LEDs você deseja analisar?", min_value=2, max_value=5, value=3)

# Valores padrão (realistas) para facilitar o teste do seu professor
valores_padrao = [
    {"cor": "Vermelho", "lambda": 650.0, "v0": 1.91},
    {"cor": "Verde", "lambda": 525.0, "v0": 2.36},
    {"cor": "Azul", "lambda": 470.0, "v0": 2.64},
    {"cor": "Amarelo", "lambda": 590.0, "v0": 2.00},
]

frequencias = []
tensoes_corte = []
cores_nomes = []

st.subheader("📊 Entrada de Dados dos LEDs")
st.write("Insira os valores medidos ou utilize os valores padrão sugeridos:")

# Cria colunas organizadas na página web para digitar os dados
col1, col2, col3 = st.columns(3)

for i in range(num_leds):
    padrao = valores_padrao[i] if i < len(valores_padrao) else {"cor": f"LED {i+1}", "lambda": 500.0, "v0": 2.0}
    
    with col1:
        cor = st.text_input(f"Cor do LED {i+1}", value=padrao["cor"], key=f"cor_{i}")
    with col2:
        lambda_nm = st.number_input(f"λ de {cor} (nm)", value=padrao["lambda"], step=10.0, key=f"lambda_{i}")
    with col3:
        v0 = st.number_input(f"Volts V0 de {cor} (V)", value=padrao["v0"], step=0.1, key=f"v0_{i}")
    
    # Cálculos físicos
    comprimento_m = lambda_nm * 1e-9
    frequencia = c / comprimento_m
    
    cores_nomes.append(cor)
    frequencias.append(frequencia)
    tensoes_corte.append(v0)

# Processamento matemático dos dados
x = np.array(frequencias)
y = np.array(tensoes_corte)

# Regressão linear (ajuste da reta)
m, b = np.polyfit(x, y, 1)
h_experimental = m * e
h_teorico = 6.62607e-34
erro = abs((h_experimental - h_teorico) / h_teorico) * 100

# Exibição dos resultados em caixas destacadas na página (Cards)
st.markdown("---")
st.subheader("🎯 Resultados da Regressão Linear")

res1, res2, res3 = st.columns(3)
res1.metric(label="Valor de h Obtido", value=f"{h_experimental:.3e} J·s")
res2.metric(label="Valor de h Teórico", value="6.626e-34 J·s")
res3.metric(label="Margem de Erro", value=f"{erro:.2f} %")

# Construção do gráfico do Matplotlib dentro da página web
fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(x, y, color="red", s=100, zorder=5, label="Dados Medidos")
ax.plot(x, m * x + b, color="blue", linewidth=2, label="Ajuste Linear (V0 vs f)")

# Legendas nos pontos do gráfico
for idx, txt in enumerate(cores_nomes):
    ax.annotate(txt, (x[idx], y[idx]), textcoords="offset points", xytext=(0,10), ha='center', fontweight='bold')

ax.set_title("Determinação da Constante de Planck", fontsize=14, fontweight='bold')
ax.set_xlabel("Frequência (Hz)", fontsize=12)
ax.set_ylabel("Tensão de Corte V0 (V)", fontsize=12)
ax.grid(True, linestyle="--", alpha=0.5)
ax.legend()

# Mostra o gráfico diretamente na interface web
st.pyplot(fig)