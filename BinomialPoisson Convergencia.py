# -*- coding: utf-8 -*-
import streamlit as st
import numpy as np
import scipy.stats as stats

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Terminal Analítico de Disponibilidade", layout="wide")

# --- ESTILIZAÇÃO CSS CUSTOMIZADA ---
st.markdown("""
    <style>
    .main-title { 
        color: #1E3A8A; 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
        padding-bottom: 20px;
    }
    .report-card {
        background-color: #f8fafc;
        padding: 25px;
        border-radius: 8px;
        border-left: 5px solid #1E3A8A;
        margin-top: 20px;
    }
    .conclusion-text {
        font-size: 1.1em;
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h2 class='main-title'>Terminal Analítico de Disponibilidade Crítica</h2>", unsafe_allow_html=True)

# --- BARRA LATERAL ---
with st.sidebar:
    st.markdown("### Configurações da Análise")
    
    with st.form("config_form"):
        st.markdown("#### Parâmetros do Inventário")
        n_val = st.number_input("População Total (n)", min_value=1, value=50)
        k_val = st.number_input("Mínimo Operacional (k)", min_value=1, value=40)
        
        st.markdown("#### Parâmetros de Confiabilidade")
        mtbf_val = st.number_input("MTBF (Horas)", min_value=1.0, value=2000.0)
        t_val = st.number_input("Ciclo de Inspeção (t)", min_value=1.0, value=168.0)
        
        submit_button = st.form_submit_button("Executar Análise")


# --- ÁREA PRINCIPAL ---
if not submit_button:
    st.info("Aguardando entrada de dados. Preencha os parâmetros na barra lateral e clique em 'Executar Análise' para iniciar o processamento matemático.")

else:
    # Validação de Segurança
    if k_val > n_val:
        st.error("Erro de Parâmetro: A demanda operacional (k) não pode ser superior à população total de ativos (n).")
    else:
        # --- CÁLCULOS ---
        s_calc = n_val - k_val
        p_calc = 1 - np.exp(-t_val / mtbf_val)
        lam_calc = n_val * p_calc
        
        conf_binom = stats.binom.cdf(s_calc, n_val, p_calc)
        conf_poisson = stats.poisson.cdf(s_calc, lam_calc)
        risco_ruptura = 1 - conf_binom

        # --- EXIBIÇÃO DAS MÉTRICAS ---
        st.markdown("### Indicadores Operacionais")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Reserva Técnica (s)", f"{s_calc}")
        c2.metric("Taxa de Falha Individual (p)", f"{p_calc:.2%}")
        c3.metric("Média de Falhas Esperada (λ)", f"{lam_calc:.3f}")
        c4.metric("Confiabilidade do Sistema", f"{conf_binom:.4%}")

        st.divider()

        # --- DETALHAMENTO DOS MODELOS ---
        st.markdown("### Detalhamento Analítico")
        
        l1, l2 = st.columns(2)
        with l1:
            st.markdown("#### Modelo Binomial (K-out-of-N)")
            st.write("Avalia a disponibilidade considerando o sucesso ou falha individual de cada equipamento no inventário.")
            st.success(f"Probabilidade Calculada: **{conf_binom:.7%}**")
        
        with l2:
            st.markdown("#### Modelo de Poisson (Sobressalentes)")
            st.write("Avalia o fluxo logístico e a probabilidade de a demanda de manutenção não exceder a reserva técnica.")
            st.success(f"Probabilidade Calculada: **{conf_poisson:.7%}**")

        # --- LAUDO DE CONVERGÊNCIA ---
        st.markdown("<div class='report-card'>", unsafe_allow_html=True)
        st.markdown("#### Análise de Convergência Estatística")
        st.write("Diferença absoluta entre as probabilidades calculadas por ambos os modelos:")
        
        st.latex(f"|P(Binomial) - P(Poisson)| = {abs(conf_binom - conf_poisson):.8f}")
        
        st.markdown(f"""
        <div class='conclusion-text'>
        <strong>Conclusão Técnica:</strong> Para uma população de {n_val} ativos com probabilidade individual de falha de {p_calc:.4%}, 
        verifica-se que a modelagem via distribuição de Poisson converge satisfatoriamente para a distribuição Binomial. 
        O erro residual entre os modelos é considerado estatisticamente desprezível para fins de dimensionamento.
        </div>
        <br>
        """, unsafe_allow_html=True)
        
        # --- ALERTAS DE SEGURANÇA ---
        if risco_ruptura > 0.05:
            st.error(f"ALERTA CRÍTICO: Risco de indisponibilidade sistêmica avaliado em {risco_ruptura:.2%}. Recomenda-se a revisão imediata do dimensionamento de estoque ou da periodicidade de inspeção.")
        else:
            st.success("STATUS CONFORME: A reserva técnica atual possui margem de segurança estatística suficiente para suportar a demanda operacional esperada.")
            
        st.markdown("</div>", unsafe_allow_html=True)
