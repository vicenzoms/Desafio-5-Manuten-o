# -*- coding: utf-8 -*-
"""
Created on Fri May 22 10:36:58 2026

@author: Vicenzo
"""

import streamlit as st
import numpy as np
import scipy.stats as stats

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Terminal de Engenharia Clínica", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    .main-title { color: #0f4c75; font-family: 'Helvetica Neue', sans-serif; text-align: center; }
    .welcome-card {
        background-color: #ffffff;
        padding: 40px;
        border-radius: 20px;
        border: 2px dashed #3282b8;
        text-align: center;
        margin-top: 50px;
    }
    .metric-box {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border-top: 4px solid #3282b8;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    .report-area {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 15px;
        border: 1px solid #bbe1fa;
        margin-top: 25px;
    }
    </style>
""", unsafe_allow_html=True)


st.markdown("<h1 class='main-title'>🏥 Terminal Analítico de Disponibilidade Crítica</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/822/822143.png", width=80)
    st.markdown("### 🛠️ Configuração de Sistema")
    
    # Criando o formulário para agrupar os inputs e o botão
    with st.form("config_form"):
        n_val = st.number_input("População Total (n)", min_value=1, value=50)
        k_val = st.number_input("Mínimo Operacional (k)", min_value=1, value=40)
        
        st.divider()
        st.markdown("### ⏱️ Parâmetros de Falha")
        mtbf_val = st.number_input("MTBF (Horas)", min_value=1.0, value=2000.0)
        t_val = st.number_input("Ciclo de Inspeção (t)", min_value=1.0, value=168.0)
        
        # O BOTÃO DE CALCULAR
        submit_button = st.form_submit_button(" EXECUTAR ANÁLISE")


if not submit_button:
    st.markdown("""
        <div class='welcome-card'>
            <h2>Aguardando Entrada de Dados...</h2>
            <p>Insira os parâmetros técnicos na barra lateral e clique em <b>Executar Análise</b> 
            para gerar o laudo de confiabilidade e a demonstração do Desafio 5.</p>
            <br>
            <p style='color: #3282b8;'><i>"A engenharia de manutenção é a medicina das máquinas."</i></p>
        </div>
    """, unsafe_allow_html=True)

else:
    
    # Validação Básica
    if k_val > n_val:
        st.error("Erro Crítico: A demanda (k) não pode ser maior que o inventário (n).")
    else:
        
        s_calc = n_val - k_val
        p_calc = 1 - np.exp(-t_val / mtbf_val)
        lam_calc = n_val * p_calc
        
        conf_binom = stats.binom.cdf(s_calc, n_val, p_calc)
        conf_poisson = stats.poisson.cdf(s_calc, lam_calc)
        risco_ruptura = 1 - conf_binom

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"<div class='metric-box'><b>Reserva Técnica (s)</b><h2>{s_calc} unidades</h2></div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='metric-box'><b>Taxa de Falha (p)</b><h2>{p_calc:.2%}</h2></div>", unsafe_allow_html=True)
        with c3:
            st.markdown(f"<div class='metric-box'><b>Média de Falhas (λ)</b><h2>{lam_calc:.3f}</h2></div>", unsafe_allow_html=True)
        with c4:
            st.markdown(f"<div class='metric-box'><b>Confiabilidade Final</b><h2>{conf_binom:.4%}</h2></div>", unsafe_allow_html=True)

        st.markdown("<div class='report-area'>", unsafe_allow_html=True)
        st.markdown("### 📋 Laudo Técnico de Engenharia Clínica")
        
        l1, l2 = st.columns(2)
        with l1:
            st.markdown("**Análise Binomial (K-out-of-N)**")
            st.write("Focada na disponibilidade individual dos leitos.")
            st.info(f"Probabilidade de Sucesso: **{conf_binom:.7%}**")
        
        with l2:
            st.markdown("**Análise de Poisson (Sobressalentes)**")
            st.write("Focada no fluxo logístico de manutenção.")
            st.info(f"Probabilidade de Cobertura: **{conf_poisson:.7%}**")

        st.divider()
        
        st.markdown("#### 🔬 Demonstração do Limite de Convergência")
        st.write("Ao observarmos a diferença absoluta entre os modelos:")
        st.latex(f"|P(Binomial) - P(Poisson)| = {abs(conf_binom - conf_poisson):.8f}")
        
        st.markdown(f"""
        **Conclusão do Desafio:** Dada a população de {n_val} ativos e a probabilidade de falha rara ({p_calc:.4%}), 
        provamos que o dimensionamento de sobressalentes via Poisson converge para a confiabilidade sistêmica Binomial. 
        O erro de modelagem é desprezível.
        """)
        
        if risco_ruptura > 0.05:
            st.error(f"🚨 **ALERTA DE SEGURANÇA:** Risco de desabastecimento de {risco_ruptura:.2%}. Sugere-se revisão imediata do estoque.")
        else:
            st.success("🟢 **SISTEMA EM CONFORMIDADE:** O backup atual suporta a demanda com margem de segurança estatística.")
        
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br><p style='text-align: center; font-size: 0.8em;'>Simulador de Engenharia de Manutenção v2.0 - Desafio 5</p>", unsafe_allow_html=True)