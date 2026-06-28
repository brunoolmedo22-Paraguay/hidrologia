"""
HydroCalc Paraná — Ferramenta Didática Interativa
Caracterização de Bacias Hidrográficas e Método Racional
Caso de estudo: Região de Foz do Iguaçu / Cascavel — PR

Autor  : Baseado na arquitetura visual de Bruno Olmedo
Licença: MIT
"""

import math
import streamlit as st
import plotly.graph_objects as go

# ──────────────────────────────────────────────────────────────────────────────
# CONFIGURAÇÃO DA PÁGINA
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="HydroCalc Paraná",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────────────────────
# PALETA E TOKENS VISUAIS  (sky-blue / branco / cinza-ardósia)
# ──────────────────────────────────────────────────────────────────────────────
ACCENT   = "#0ea5e9"   # sky-500
ACCENT_D = "#0284c7"   # sky-600
ACCENT_L = "#e0f2fe"   # sky-100
BG_PAGE  = "#f0f4f8"
BG_CARD  = "#ffffff"
TEXT_PRI = "#0f172a"
TEXT_SEC = "#64748b"
SUCCESS  = "#10b981"   # emerald-500
WARNING  = "#f59e0b"   # amber-500
DANGER   = "#ef4444"   # red-500

# ──────────────────────────────────────────────────────────────────────────────
# CSS GLOBAL
# ──────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
/* ── base ──────────────────────────────────────────── */
html, body, [class*="css"] {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Inter', sans-serif;
    background-color: {BG_PAGE};
}}

/* ── sidebar ─────────────────────────────────────────── */
section[data-testid="stSidebar"] {{
    background: {BG_CARD} !important;
    border-right: 1px solid #e2e8f0 !important;
}}
section[data-testid="stSidebar"] > div {{
    padding-top: 1.4rem;
}}

/* ── título sidebar ──────────────────────────────────── */
.sb-brand {{
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 0 4px 14px;
    border-bottom: 1px solid #e2e8f0;
    margin-bottom: 16px;
}}
.sb-brand-icon {{
    font-size: 26px;
    line-height: 1;
}}
.sb-brand-title {{
    font-size: 17px;
    font-weight: 800;
    color: {TEXT_PRI};
    letter-spacing: -0.4px;
    line-height: 1.15;
}}
.sb-brand-sub {{
    font-size: 10.5px;
    color: {TEXT_SEC};
    letter-spacing: 0.04em;
    text-transform: uppercase;
    font-weight: 600;
}}

/* ── label de seção sidebar ───────────────────────────── */
.sb-label {{
    font-size: 9.5px;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: {TEXT_SEC};
    padding: 16px 4px 6px;
    display: block;
}}

/* ── cards de destaque ──────────────────────────────── */
.info-card {{
    background: {BG_CARD};
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 16px;
    box-shadow: 0 2px 8px rgba(14,165,233,0.05);
}}
.info-card-accent {{
    border-left: 4px solid {ACCENT};
    background: {ACCENT_L};
    border-radius: 0 14px 14px 0;
    padding: 16px 20px;
    margin-bottom: 16px;
}}

/* ── chip / badge ──────────────────────────────────── */
.chip {{
    display: inline-flex;
    align-items: center;
    gap: 7px;
    background: rgba(14,165,233,0.09);
    border: 1px solid rgba(14,165,233,0.22);
    border-radius: 20px;
    padding: 4px 14px;
    margin-bottom: 18px;
    font-size: 12.5px;
    font-weight: 700;
    color: {ACCENT_D};
    letter-spacing: 0.03em;
}}

/* ── título de página ───────────────────────────────── */
.page-title {{
    font-size: 26px;
    font-weight: 800;
    color: {TEXT_PRI};
    letter-spacing: -0.5px;
    margin-bottom: 4px;
    line-height: 1.2;
}}
.page-subtitle {{
    font-size: 14px;
    color: {TEXT_SEC};
    margin-bottom: 28px;
    line-height: 1.55;
}}

/* ── resultado destaque ─────────────────────────────── */
.result-box {{
    background: linear-gradient(135deg, {ACCENT}, {ACCENT_D});
    color: white;
    border-radius: 16px;
    padding: 24px 28px;
    text-align: center;
    box-shadow: 0 8px 28px rgba(14,165,233,0.28);
}}
.result-box .label {{
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    opacity: 0.85;
    margin-bottom: 6px;
}}
.result-box .value {{
    font-size: 44px;
    font-weight: 900;
    letter-spacing: -1px;
    line-height: 1;
}}
.result-box .unit {{
    font-size: 18px;
    font-weight: 500;
    opacity: 0.80;
    margin-left: 4px;
}}

/* ── step box (memória de cálculo) ───────────────────── */
.step-box {{
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 12px;
}}
.step-title {{
    font-size: 12px;
    font-weight: 700;
    color: {ACCENT_D};
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 8px;
}}

/* ── alerta personalizado ──────────────────────────── */
.alert-warning {{
    background: #fffbeb;
    border: 1px solid #fde68a;
    border-left: 4px solid {WARNING};
    border-radius: 10px;
    padding: 12px 16px;
    color: #78350f;
    font-size: 13.5px;
    margin: 12px 0;
}}
.alert-info {{
    background: {ACCENT_L};
    border: 1px solid #bae6fd;
    border-left: 4px solid {ACCENT};
    border-radius: 10px;
    padding: 12px 16px;
    color: #0c4a6e;
    font-size: 13.5px;
    margin: 12px 0;
}}

/* ── separador com título ──────────────────────────── */
.section-divider {{
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 24px 0 16px;
}}
.section-divider hr {{
    flex: 1;
    border: none;
    border-top: 1px solid #e2e8f0;
    margin: 0;
}}
.section-divider span {{
    font-size: 11px;
    font-weight: 700;
    color: {TEXT_SEC};
    letter-spacing: 0.1em;
    text-transform: uppercase;
    white-space: nowrap;
}}

/* ── botões de nav (sidebar) — estilo referência ─────── */
section[data-testid="stSidebar"] button {{
    border-radius: 10px !important;
    font-size: 14px !important;
    letter-spacing: -0.1px !important;
    transition: all 0.15s ease !important;
}}
section[data-testid="stSidebar"] button[kind="secondary"] {{
    background: rgba(14,165,233,0.06) !important;
    border: none !important;
    color: {ACCENT_D} !important;
    font-weight: 500 !important;
}}
section[data-testid="stSidebar"] button[kind="secondary"]:hover {{
    background: rgba(14,165,233,0.12) !important;
}}
section[data-testid="stSidebar"] button[kind="primary"] {{
    background: linear-gradient(135deg, {ACCENT}, {ACCENT_D}) !important;
    border: none !important;
    box-shadow: 0 3px 12px rgba(14,165,233,0.35) !important;
    font-weight: 600 !important;
    color: white !important;
}}

/* ── tabs — aparência limpa ────────────────────────── */
button[data-baseweb="tab"] {{
    font-weight: 600 !important;
    font-size: 13.5px !important;
}}
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
# DADOS IDF POR CIDADE — Paraná (SUDERHSA)
# ──────────────────────────────────────────────────────────────────────────────
DADOS_CIDADES_IDF = {
    "Cascavel":      {"K": 1062.92,  "a": 0.141, "b": 5.0,    "c": 0.776},
    "Curitiba":      {"K": 5949.995, "a": 0.217, "b": 26.0,   "c": 1.150},
    "Foz do Iguaçu": {"K": 2853.479, "a": 0.125, "b": 25.674, "c": 0.925},
    "Guarapuava":    {"K": 1039.68,  "a": 0.171, "b": 10.0,   "c": 0.799},
    "Londrina":      {"K": 3132.560, "a": 0.093, "b": 30.0,   "c": 0.939},
    "Medianeira":    {"K": 2886.690, "a": 0.124, "b": 26.0,   "c": 0.927},
    "Paranaguá":     {"K": 2052.13,  "a": 0.157, "b": 23.246, "c": 0.876},
    "Pato Branco":   {"K": 879.441,  "a": 0.152, "b": 9.0,    "c": 0.732},
    "Ponta Grossa":  {"K": 1902.388, "a": 0.152, "b": 21.0,   "c": 0.893},
    "Personalizado": {"K": 1062.92,  "a": 0.141, "b": 5.0,    "c": 0.776},
}

# ──────────────────────────────────────────────────────────────────────────────
# SESSION STATE — inicialização das variáveis compartilhadas
# ──────────────────────────────────────────────────────────────────────────────
defaults = {
    "area_km2":    1.2,
    "L_m":         1795.0,
    "S":           0.02,
    "T_anos":      10,
    "K":           1062.92,
    "a_idf":       0.141,
    "b_idf":       5.0,
    "c_idf":       0.776,
    "pct_urban":   30,
    "C_urb":       0.90,
    "C_rur":       0.40,
    "cidade_idf":  "Cascavel",
    "pagina_ativa": "estudo",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ──────────────────────────────────────────────────────────────────────────────
# SIDEBAR — nav_button igual ao estilo da referência
# ──────────────────────────────────────────────────────────────────────────────
def nav_button(label: str, key_val: str):
    """Botão de navegação com estado primário/secundário — igual à referência."""
    active = st.session_state.get("pagina_ativa") == key_val
    if st.sidebar.button(
        label,
        type="primary" if active else "secondary",
        key=f"nav_{key_val}",
        use_container_width=True,
    ):
        st.session_state["pagina_ativa"] = key_val
        st.rerun()


with st.sidebar:
    st.markdown("""
    <div class="sb-brand">
        <span class="sb-brand-icon">💧</span>
        <div>
            <div class="sb-brand-title">HydroCalc<br>Paraná</div>
            <div class="sb-brand-sub">Hidrologia Aplicada</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<span class="sb-label">Navegação</span>', unsafe_allow_html=True)
    nav_button("🗺️  Estudo de Caso", "estudo")
    nav_button("📐  Simulador Hidrológico", "simulador")

    st.markdown("---")
    st.markdown("""
    <div style="font-size:11.5px; color:#94a3b8; line-height:1.7; padding: 0 4px;">
        <b style="color:#64748b;">Método Racional</b><br>
        Fórmula: Q = C·i·A / 3,6<br><br>
        <b style="color:#64748b;">Tempo de Concentração</b><br>
        Kirpich (1940)<br><br>
        <b style="color:#64748b;">IDF — PR (SUDERHSA)</b><br>
        9 cidades disponíveis
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.caption("Desenvolvido para fins didáticos · PPGIES / UNILA")


# ──────────────────────────────────────────────────────────────────────────────
# HELPERS — funções de cálculo
# ──────────────────────────────────────────────────────────────────────────────
def calc_tc_kirpich(L_m: float, S: float) -> float:
    """
    Tempo de concentração — Fórmula de Kirpich (1940).
    tc = 0,0195 · (L^0,77) / (S^0,385)
    L  : comprimento do talvegue [m]
    S  : declividade média [m/m]
    Retorna tc em minutos.
    """
    if S <= 0 or L_m <= 0:
        return 0.0
    tc_min = 0.0195 * (L_m ** 0.77) / (S ** 0.385)
    return tc_min


def calc_idf(K: float, a: float, T: float, tc_min: float, b: float, c: float) -> float:
    """
    Intensidade de chuva pela equação IDF potencial.
    i = K · T^a / (tc + b)^c
    Retorna i em mm/h.
    """
    if (tc_min + b) <= 0:
        return 0.0
    i = K * (T ** a) / ((tc_min + b) ** c)
    return i


def calc_C_medio(pct_urban: int, C_urb: float, C_rur: float) -> float:
    """Coeficiente de escoamento médio ponderado pela área."""
    f_urb = pct_urban / 100.0
    f_rur = 1.0 - f_urb
    return f_urb * C_urb + f_rur * C_rur


def calc_Q_racional(C: float, i_mm_h: float, A_km2: float) -> float:
    """
    Método Racional: Q = C · i · A / 3,6
    C      : coeficiente de escoamento (adimensional)
    i      : intensidade [mm/h]
    A      : área [km²]
    Retorna Q em m³/s.
    """
    return (C * i_mm_h * A_km2) / 3.6


def plotly_config() -> dict:
    """Configuração padrão do Plotly para tema limpo."""
    return dict(
        paper_bgcolor="white",
        plot_bgcolor="#f8fafc",
        font=dict(family="'Segoe UI', sans-serif", color=TEXT_PRI),
        margin=dict(t=50, b=40, l=50, r=30),
        hoverlabel=dict(bgcolor="white", bordercolor="#e2e8f0"),
    )


# ──────────────────────────────────────────────────────────────────────────────
# PAGE 1 — ESTUDO DE CASO: BACIA DO PARANÁ
# ──────────────────────────────────────────────────────────────────────────────
def render_page_estudo():
    st.markdown(
        f'<div class="chip">🗺️ Estudo de Caso</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-title">Bacia Hidrográfica do Rio Paraná</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">'
        'Caracterização físico-climática e análise de uso do solo da maior bacia hidrográfica '
        'da América do Sul em território brasileiro — com foco na região de Foz do Iguaçu e Cascavel.'
        '</div>',
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3 = st.tabs([
        "🏔️  Caracterização Física",
        "🌧️  Clima e Regime Hidrológico",
        "🌿  Uso do Solo e Impactos",
    ])

    # ── ABA 1 — CARACTERIZAÇÃO FÍSICA ─────────────────────────────────
    with tab1:
        st.markdown("### O que é uma Bacia Hidrográfica?")

        st.markdown("""
        <div class="info-card">
        Uma <b>bacia hidrográfica</b> é definida como a área geográfica delimitada topograficamente
        que drena toda a precipitação recebida para um único ponto de exutório — denominado
        <em>seção de controle</em> ou <em>exutório</em>. Trata-se da unidade fundamental de
        planejamento em recursos hídricos, pois todos os processos do ciclo hidrológico
        (precipitação, interceptação, infiltração, escoamento superficial e subterrâneo) se
        manifestam e interagem dentro dos seus limites.
        </div>
        """, unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("""
            #### Divisores de Água
            Os **divisores de água** (ou *watersheds*) são as linhas imaginárias que separam
            bacias adjacentes, conectando os pontos de maior cota do terreno. Toda gota de chuva
            que cai de um lado de um divisor irá drenar para uma bacia diferente da gota que
            cai do outro lado.

            Em regiões de relevo mais suave — como o *Terceiro Planalto Paranaense* —
            os divisores são por vezes difíceis de identificar em campo, o que torna
            fundamental a análise de Modelos Digitais de Elevação (MDE/DEM).
            """)
        with col_b:
            st.markdown("""
            #### Parâmetros Morfométricos Essenciais
            | Parâmetro | Descrição |
            |-----------|-----------|
            | **Área (A)** | Superfície total delimitada pelos divisores |
            | **Perímetro (P)** | Extensão do divisor de águas |
            | **Comprimento do talvegue (L)** | Maior curso d'água da bacia |
            | **Declividade média (S)** | Gradiente hidráulico do talvegue |
            | **Coeficiente de compacidade (Kc)** | Razão entre forma e círculo equivalente |
            | **Fator de forma (Kf)** | Susceptibilidade a cheias concentradas |
            """)

        st.markdown("---")
        st.markdown("### A Bacia do Rio Paraná")

        col1, col2, col3 = st.columns(3)
        col1.metric("Área total", "891.309 km²", help="Porção brasileira da bacia")
        col2.metric("Extensão do Rio Paraná", "≈ 4.880 km", help="Do nascente ao Río de la Plata")
        col3.metric("Países abrangidos", "3", help="Brasil, Paraguai e Argentina")

        st.markdown("""
        <div class="info-card-accent">
        A <b>Bacia do Rio Paraná</b> é a segunda maior da América do Sul (superada apenas
        pela Amazônica) e possui papel estratégico na geração de energia elétrica brasileira.
        Apenas a <b>Usina Hidrelétrica de Itaipu Binacional</b>, localizada em Foz do Iguaçu/PR,
        responde por aproximadamente <b>10–15% de toda a energia elétrica consumida no Brasil</b>
        e cerca de 90% da demanda paraguaia.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### Sub-bacia do Rio Iguaçu")
        st.markdown("""
        O **Rio Iguaçu** é o maior afluente exclusivamente paranaense do Rio Paraná, com
        cerca de **910 km** de extensão e uma área de drenagem de **~70.800 km²**. Nasce
        na Serra do Mar, atravessa o estado do Paraná de leste a oeste e deságua no Rio
        Paraná na fronteira tríplice (Brasil, Argentina, Paraguai), formando as famosas
        **Cataratas do Iguaçu** — Patrimônio Natural da Humanidade pela UNESCO.

        A região do **Terceiro Planalto Paranaense** (onde se situam Cascavel e Foz do Iguaçu)
        é caracterizada por substrato basáltico da Formação Serra Geral, solos de alta
        fertilidade (Latossolos Roxos / Nitossolos Vermelhos) e relevo suave-ondulado com
        altitude variando entre **200 e 900 metros**.
        """)

    # ── ABA 2 — CLIMA E REGIME HIDROLÓGICO ───────────────────────────
    with tab2:
        st.markdown("### Clima do Oeste do Paraná")

        st.markdown("""
        <div class="info-card">
        A região de Foz do Iguaçu e Cascavel possui clima classificado como <b>Cfa</b>
        (Subtropical Úmido, segundo Köppen-Geiger) — subtropical com verões quentes e
        sem estação seca definida. A ausência de uma seca pronunciada é uma característica
        fundamental que diferencia esta região do interior nordestino e influencia
        diretamente o regime hidrológico.
        </div>
        """, unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("""
            #### Pluviometria
            - **Precipitação média anual:** 1.600 – 1.900 mm
            - **Distribuição:** relativamente uniforme ao longo do ano
            - **Meses mais chuvosos:** outubro, novembro, dezembro (primavera austral)
            - **Meses mais secos:** julho e agosto (inverno), porém sem déficit hídrico crítico
            - **Intensidade máxima em 24h:** eventos de 80–120 mm registrados historicamente

            A equação IDF (**Intensidade–Duração–Frequência**) para Cascavel,
            derivada de dados pluviográficos da SUDERHSA, possui coeficientes
            bem estabelecidos, utilizados como padrão nesta ferramenta.
            """)
        with col_b:
            st.markdown("""
            #### Sazonalidade e Regime de Cheias
            - **Período de maior risco de cheias:** outubro a março
            - **Causa principal das cheias:** precipitações convectivas de alta intensidade
              e curta duração associadas a Sistemas Convectivos de Mesoescala (SCM)
            - **El Niño:** provoca aumento de 20–40% na precipitação invernal
            - **La Niña:** redução da precipitação, especialmente no verão
            - **Temperatura média anual:** 20–22 °C (Foz) / 19–21 °C (Cascavel)
            - **Umidade relativa:** 70–80%
            """)

        st.markdown("---")
        st.markdown("""
        <div class="alert-warning">
        <b>⚠️ Relevância para o Dimensionamento:</b> A alta variabilidade interanual da
        precipitação — amplificada pelos eventos ENOS (El Niño–Oscilação Sul) — torna
        fundamental o uso de <b>análise de frequência estatística</b> (período de retorno T)
        no dimensionamento de obras hidráulicas. Um bueiro subdimensionado para Tr = 5 anos
        poderá ser sobrecarregado com frequência muito maior do que a desejada.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### O que é o Período de Retorno (Tr)?")
        st.markdown("""
        O **Período de Retorno** (ou Tempo de Recorrência), expresso em anos, representa
        o **intervalo médio de tempo** entre ocorrências iguais ou superiores a um determinado
        evento hidrológico. É o inverso da probabilidade de excedência anual:

        $$P_{excedência} = \\frac{1}{T_r}$$

        Portanto, uma chuva de Tr = 10 anos tem **10% de probabilidade de ser igualada ou
        superada em qualquer ano**. Para obras de pequeno porte (bueiros, sarjetas), adota-se
        geralmente Tr = 5 a 25 anos. Para grandes barragens, Tr ≥ 10.000 anos.
        """)

    # ── ABA 3 — USO DO SOLO E IMPACTOS ───────────────────────────────
    with tab3:
        st.markdown("### Uso do Solo e Impacto no Ciclo Hidrológico")

        st.markdown("""
        <div class="info-card">
        O <b>escoamento superficial direto</b> (runoff) é a parcela da precipitação que,
        após atender às demandas de interceptação vegetal, infiltração no solo e retenção
        em depressões, escoa sobre a superfície em direção aos cursos d'água. A urbanização
        altera profundamente todos esses processos.
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            #### 🌿 Bacia Natural / Florestal
            Na cobertura vegetal original (*Floresta Estacional Semidecidual* —
            Mata Atlântica interior), o ciclo hidrológico funciona de forma
            amortecida:

            - A **interceptação foliar** retém 15–30% da chuva
            - A **serapilheira** (manta orgânica) aumenta a rugosidade e favorece a infiltração
            - Solos com alta macroporosidade (Latossolos) absorvem grande volume
            - O escoamento é **lento e distribuído no tempo** (hidrograma achatado)
            - **C típico: 0,10 – 0,35**
            """)
        with col2:
            st.markdown("""
            #### 🏙️ Bacia Urbanizada
            A substituição da vegetação por superfícies impermeáveis (asfalto, concreto,
            telhados) e a canalização de cursos d'água geram:

            - **Eliminação da interceptação** e da evapotranspiração
            - **Redução drástica da infiltração** (< 5% em áreas densamente impermeabilizadas)
            - Escoamento **rápido e concentrado** (hidrograma estreito e alto)
            - Aumento do **pico de cheia** em 3 a 8 vezes
            - Antecipação do tempo de concentração
            - **C típico: 0,70 – 0,95**
            """)

        st.markdown("---")
        st.markdown("### Histórico de Uso do Solo — Região de Foz do Iguaçu / Cascavel")
        st.markdown("""
        A região oeste do Paraná passou por transformações aceleradas a partir da
        **colonização da década de 1950–1970**, quando extensas áreas de floresta foram
        convertidas em lavouras de café, soja e milho. Com o crescimento urbano de
        Cascavel e Foz do Iguaçu — cidades com crescimento demográfico acima da média
        nacional —, áreas agrícolas periurbanas foram progressivamente substituídas
        por loteamentos residenciais e zonas industriais.

        Os principais impactos identificados nos estudos hidrológicos da região incluem:

        1. **Aumento da frequência de inundações urbanas** em Foz do Iguaçu, especialmente
           nas bacias dos Córregos São João e Tamanduá.
        2. **Redução da recarga de aquíferos**, com impactos na disponibilidade hídrica
           subterrânea do Sistema Aquífero Serra Geral.
        3. **Assoreamento de cursos d'água** pela erosão de solos expostos em obras e
           loteamentos sem controle adequado.
        """)

        st.markdown("""
        <div class="alert-info">
        <b>💡 Conexão com o Simulador:</b> O coeficiente de escoamento superficial
        <b>C</b> do Método Racional é a variável que traduz quantitativamente esse impacto
        da urbanização. No simulador da próxima página, você poderá ajustar a percentagem
        de área urbanizada e observar como a vazão de pico responde a essa mudança — de forma
        direta e visual.
        </div>
        """, unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
# PAGE 2 — SIMULADOR HIDROLÓGICO
# ──────────────────────────────────────────────────────────────────────────────
def render_page_simulador():
    st.markdown(
        f'<div class="chip">📐 Simulador Hidrológico</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-title">Método Racional — Estimativa de Vazão Máxima</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">'
        'Insira os parâmetros da bacia nas abas abaixo. Os resultados são calculados em tempo real '
        'e consolidados na aba de Resultados. Caso de estudo padrão: micro-bacia urbana em Cascavel/PR.'
        '</div>',
        unsafe_allow_html=True,
    )

    tab_morfo, tab_idf, tab_solo, tab_result = st.tabs([
        "1️⃣  Dados Morfométricos",
        "2️⃣  Chuva Intensa (IDF)",
        "3️⃣  Uso do Solo (C)",
        "4️⃣  Resultados e Conclusão",
    ])

    # ── ABA 1 — DADOS MORFOMÉTRICOS ─────────────────────────────────────
    with tab_morfo:
        st.markdown("### Parâmetros Físicos da Bacia")
        st.markdown("""
        Insira as características morfométricas da bacia de drenagem. Os valores padrão
        representam uma micro-bacia hipotética típica da região periurbana de Cascavel/PR.
        """)

        st.markdown('<div class="section-divider"><hr/><span>Geometria da bacia</span><hr/></div>',
                    unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            area = st.number_input(
                label="Área da Bacia — A (km²)",
                min_value=0.01,
                max_value=5000.0,
                value=st.session_state["area_km2"],
                step=0.1,
                format="%.2f",
                help="Área total delimitada pelos divisores de água.",
                key="area_km2",
            )
        with col2:
            L = st.number_input(
                label="Comprimento do Talvegue — L (m)",
                min_value=10.0,
                max_value=500_000.0,
                value=st.session_state["L_m"],
                step=10.0,
                format="%.1f",
                help="Comprimento do curso d'água principal, da cabeceira ao exutório.",
                key="L_m",
            )

        col3, col4 = st.columns(2)
        with col3:
            S = st.number_input(
                label="Declividade Média do Talvegue — S (m/m)",
                min_value=0.0001,
                max_value=0.50,
                value=st.session_state["S"],
                step=0.001,
                format="%.4f",
                help="Gradiente médio ΔH/L do curso d'água principal.",
                key="S",
            )
        with col4:
            T = st.number_input(
                label="Período de Retorno — Tr (anos)",
                min_value=1,
                max_value=10_000,
                value=st.session_state["T_anos"],
                step=1,
                help="Tempo de recorrência para o evento de projeto.",
                key="T_anos",
            )

        st.markdown('<div class="section-divider"><hr/><span>Guia de referência</span><hr/></div>',
                    unsafe_allow_html=True)

        col_ref1, col_ref2 = st.columns(2)
        with col_ref1:
            st.markdown("""
            **Período de Retorno recomendado por tipo de obra** (NBR/DNIT):
            | Obra | Tr recomendado |
            |------|----------------|
            | Sarjeta / meio-fio | 5 anos |
            | Bueiro simples | 10–25 anos |
            | Bueiro duplo | 25–50 anos |
            | Galeria pluvial urbana | 25–100 anos |
            | Piscinão / barragem de detenção | 100–500 anos |
            """)
        with col_ref2:
            st.markdown("""
            **Faixas típicas de declividade (S)**:
            | Relevo | S (m/m) |
            |--------|---------|
            | Plano | < 0,005 |
            | Suave ondulado | 0,005 – 0,02 |
            | Ondulado | 0,02 – 0,05 |
            | Forte ondulado | 0,05 – 0,15 |
            | Montanhoso | > 0,15 |
            """)

        st.success(
            f"✅ **Parâmetros registrados:** A = {st.session_state['area_km2']:.2f} km² | "
            f"L = {st.session_state['L_m']:.0f} m | "
            f"S = {st.session_state['S']:.4f} m/m | "
            f"Tr = {st.session_state['T_anos']} anos"
        )

    # ── ABA 2 — CHUVA INTENSA (IDF) ─────────────────────────────────────
    with tab_idf:
        st.markdown("### Equação Intensidade–Duração–Frequência (IDF)")

        # ── Tempo de concentração ───────────────────────────────────────
        st.markdown('<div class="section-divider"><hr/><span>Tempo de Concentração — Kirpich</span><hr/></div>',
                    unsafe_allow_html=True)

        tc_min = calc_tc_kirpich(st.session_state["L_m"], st.session_state["S"])
        tc_h   = tc_min / 60.0

        col_form, col_result = st.columns([1.6, 1])
        with col_form:
            st.markdown("**Fórmula de Kirpich (1940):**")
            st.latex(r"t_c = 0{,}0195 \cdot \frac{L^{0,77}}{S^{0,385}}")
            st.markdown(r"""
            Onde:
            - $L$ = comprimento do talvegue \[m\]
            - $S$ = declividade média \[m/m\]
            - $t_c$ = tempo de concentração \[min\]

            A fórmula de Kirpich foi desenvolvida originalmente para bacias rurais com
            até 45 km² e é amplamente empregada no dimensionamento de drenagem urbana
            e rural no Brasil.
            """)
        with col_result:
            st.metric("Tempo de Concentração", f"{tc_min:.2f} min", f"= {tc_h:.3f} h")
            if tc_min < 5:
                st.markdown('<div class="alert-warning">⚠️ tc < 5 min: verifique os parâmetros de entrada.</div>',
                            unsafe_allow_html=True)
            elif tc_min > 360:
                st.markdown('<div class="alert-warning">⚠️ tc > 6 h: revise se o Método Racional é adequado.</div>',
                            unsafe_allow_html=True)
            else:
                st.markdown('<div class="alert-info">✅ tc dentro da faixa recomendada para o Método Racional.</div>',
                            unsafe_allow_html=True)

        # ── Coeficientes IDF ────────────────────────────────────────────
        st.markdown('<div class="section-divider"><hr/><span>Coeficientes da equação IDF — Paraná (SUDERHSA)</span><hr/></div>',
                    unsafe_allow_html=True)

        st.markdown("""
        Selecione uma cidade do Paraná para carregar automaticamente os coeficientes IDF
        calibrados pela SUDERHSA/SIMEPAR. Escolha **Personalizado** para inserir valores
        manualmente para qualquer outra localidade.
        """)

        # ── Selectbox de cidade ─────────────────────────────────────────
        cidades_opcoes = list(DADOS_CIDADES_IDF.keys())
        idx_cidade = cidades_opcoes.index(st.session_state["cidade_idf"])                      if st.session_state["cidade_idf"] in cidades_opcoes else 0

        cidade_sel = st.selectbox(
            "📍 Cidade de referência (IDF)",
            options=cidades_opcoes,
            index=idx_cidade,
            key="cidade_idf",
            help="Selecione a cidade para carregar os coeficientes IDF calibrados. "
                 "Escolha Personalizado para editar livremente.",
        )

        # Ao mudar de cidade (exceto Personalizado), atualiza K/a/b/c no session_state
        if cidade_sel != "Personalizado":
            coefs = DADOS_CIDADES_IDF[cidade_sel]
            st.session_state["K"]     = coefs["K"]
            st.session_state["a_idf"] = coefs["a"]
            st.session_state["b_idf"] = coefs["b"]
            st.session_state["c_idf"] = coefs["c"]

        disabled_inputs = (cidade_sel != "Personalizado")
        if disabled_inputs:
            st.markdown(
                '<div class="alert-info">✅ Coeficientes carregados automaticamente para <b>' +
                cidade_sel + '</b>. Selecione <b>Personalizado</b> para editar manualmente.</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="alert-warning">✏️ Modo personalizado — insira os coeficientes manualmente abaixo.</div>',
                unsafe_allow_html=True,
            )

        col_k, col_a, col_b, col_c = st.columns(4)
        with col_k:
            K = st.number_input(
                "K", min_value=1.0, max_value=9999.0,
                value=st.session_state["K"], step=1.0, format="%.2f",
                key="K",
                help="Coeficiente de escala da equação IDF.",
                disabled=disabled_inputs,
            )
        with col_a:
            a_idf = st.number_input(
                "a", min_value=0.001, max_value=1.0,
                value=st.session_state["a_idf"], step=0.001, format="%.3f",
                key="a_idf",
                help="Expoente do período de retorno.",
                disabled=disabled_inputs,
            )
        with col_b:
            b_idf = st.number_input(
                "b", min_value=0.0, max_value=100.0,
                value=st.session_state["b_idf"], step=0.5, format="%.1f",
                key="b_idf",
                help="Coeficiente de ajuste da duração (minutos).",
                disabled=disabled_inputs,
            )
        with col_c:
            c_idf = st.number_input(
                "c", min_value=0.1, max_value=2.0,
                value=st.session_state["c_idf"], step=0.001, format="%.3f",
                key="c_idf",
                help="Expoente de decaimento da intensidade com a duração.",
                disabled=disabled_inputs,
            )

        st.markdown("**Equação IDF utilizada:**")
        st.latex(
            r"i = \frac{K \cdot T^a}{(t_c + b)^c} \quad \left[\frac{mm}{h}\right]"
        )

        # ── Cálculo da intensidade ──────────────────────────────────────
        i_mm_h = calc_idf(
            st.session_state["K"],
            st.session_state["a_idf"],
            st.session_state["T_anos"],
            tc_min,
            st.session_state["b_idf"],
            st.session_state["c_idf"],
        )

        st.markdown("---")
        col_metric, col_ctx = st.columns([1, 2])
        with col_metric:
            st.metric(
                label="Intensidade de Chuva de Projeto — i",
                value=f"{i_mm_h:.2f} mm/h",
                help="Intensidade média da chuva para o tc e Tr definidos.",
            )
        with col_ctx:
            st.markdown(f"""
            <div class="alert-info">
            Substituindo na equação IDF os valores <b>Tr = {st.session_state['T_anos']} anos</b>
            e <b>t<sub>c</sub> = {tc_min:.2f} min</b>, obtém-se uma intensidade de projeto
            de <b>{i_mm_h:.2f} mm/h</b>. Isso significa que, durante o período crítico de
            concentração da bacia, a chuva de projeto precipita em média <b>{i_mm_h:.2f} mm</b>
            por hora sobre toda a área.
            </div>
            """, unsafe_allow_html=True)

        # ── Curva IDF visualizada ───────────────────────────────────────
        st.markdown('<div class="section-divider"><hr/><span>Curvas IDF para diferentes Tr</span><hr/></div>',
                    unsafe_allow_html=True)

        duracoes = list(range(5, 181, 5))
        trs_plot = [2, 5, 10, 25, 50, 100]
        cores    = ["#94a3b8", "#64748b", ACCENT, "#0284c7", "#7c3aed", "#b91c1c"]

        fig_idf = go.Figure()
        for tr_val, cor in zip(trs_plot, cores):
            intensidades = [
                calc_idf(
                    st.session_state["K"], st.session_state["a_idf"],
                    tr_val, d,
                    st.session_state["b_idf"], st.session_state["c_idf"]
                )
                for d in duracoes
            ]
            lw = 3 if tr_val == st.session_state["T_anos"] else 1.5
            dash = "solid" if tr_val == st.session_state["T_anos"] else "dot"
            fig_idf.add_trace(go.Scatter(
                x=duracoes, y=intensidades,
                name=f"Tr = {tr_val} anos",
                line=dict(color=cor, width=lw, dash=dash),
                mode="lines",
            ))

        # Ponto de projeto
        fig_idf.add_trace(go.Scatter(
            x=[tc_min], y=[i_mm_h],
            name="Ponto de projeto",
            mode="markers",
            marker=dict(color=ACCENT, size=12, symbol="circle",
                        line=dict(color="white", width=2)),
        ))

        fig_idf.update_layout(
            **plotly_config(),
            title=dict(text="Curvas IDF — Cascavel/PR", font=dict(size=14, weight="bold")),
            xaxis=dict(title="Duração da chuva (min)", gridcolor="#e2e8f0"),
            yaxis=dict(title="Intensidade i (mm/h)", gridcolor="#e2e8f0"),
            legend=dict(orientation="h", y=-0.25, x=0.5, xanchor="center"),
            height=380,
        )
        st.plotly_chart(fig_idf, use_container_width=True)

    # ── ABA 3 — USO DO SOLO / COEFICIENTE C ──────────────────────────────
    with tab_solo:
        st.markdown("### Coeficiente de Escoamento Superficial — C")
        st.markdown("""
        O coeficiente **C** (adimensional) representa a fração da precipitação que se
        converte em escoamento superficial direto. No Método Racional, ele é o
        parâmetro que sintetiza o efeito combinado da cobertura do solo, declividade
        e tipo de solo.
        """)

        st.markdown('<div class="section-divider"><hr/><span>Composição do uso do solo</span><hr/></div>',
                    unsafe_allow_html=True)

        pct_urban = st.slider(
            label="Percentagem de Área Urbanizada (%)",
            min_value=0, max_value=100,
            value=st.session_state["pct_urban"],
            step=1,
            key="pct_urban",
            help="Deslize para simular diferentes graus de urbanização da bacia.",
        )
        pct_rural = 100 - pct_urban

        col_u, col_r = st.columns(2)
        with col_u:
            st.metric("Área Urbana", f"{pct_urban} %", f"{st.session_state['area_km2'] * pct_urban / 100:.3f} km²")
            C_urb = st.number_input(
                "Coeficiente C — Área Urbana",
                min_value=0.0, max_value=1.0,
                value=st.session_state["C_urb"],
                step=0.01, format="%.2f",
                key="C_urb",
                help="Áreas impermeabilizadas densas: 0,80–0,95. Residencial de baixa densidade: 0,40–0,60.",
            )
        with col_r:
            st.metric("Área Rural / Vegetada", f"{pct_rural} %", f"{st.session_state['area_km2'] * pct_rural / 100:.3f} km²")
            C_rur = st.number_input(
                "Coeficiente C — Área Rural",
                min_value=0.0, max_value=1.0,
                value=st.session_state["C_rur"],
                step=0.01, format="%.2f",
                key="C_rur",
                help="Pastagem / cultivo: 0,30–0,55. Floresta densa: 0,10–0,30.",
            )

        # ── Cálculo C médio ────────────────────────────────────────────
        C_medio = calc_C_medio(pct_urban, C_urb, C_rur)

        st.markdown("---")
        st.markdown("**Fórmula do C ponderado por área:**")
        st.latex(
            r"C_{médio} = \frac{\sum C_i \cdot A_i}{A_{total}} "
            r"= \frac{C_{urb} \cdot A_{urb} + C_{rur} \cdot A_{rur}}{A_{total}}"
        )

        col_cm, col_interp = st.columns([1, 2])
        with col_cm:
            st.metric(
                "C médio ponderado",
                f"{C_medio:.3f}",
                delta=f"{'↑' if C_medio > 0.5 else '↓'} {'urbanizado' if C_medio > 0.5 else 'permeável'}",
            )
        with col_interp:
            if C_medio < 0.30:
                interp = "🌿 Bacia predominantemente natural. Escoamento baixo, boa capacidade de infiltração."
                cor_interp = "alert-info"
            elif C_medio < 0.55:
                interp = "🌾 Bacia mista, uso agropecuário relevante. Escoamento moderado."
                cor_interp = "alert-info"
            elif C_medio < 0.75:
                interp = "⚠️ Bacia com urbanização significativa. Atenção ao risco de inundação."
                cor_interp = "alert-warning"
            else:
                interp = "🏙️ Bacia altamente urbanizada. Alto risco de enchentes e picos de cheia elevados."
                cor_interp = "alert-warning"
            st.markdown(f'<div class="{cor_interp}">{interp}</div>', unsafe_allow_html=True)

        # ── Tabela de referência ──────────────────────────────────────
        st.markdown('<div class="section-divider"><hr/><span>Valores de C por tipo de superfície (referência)</span><hr/></div>',
                    unsafe_allow_html=True)

        col_ref1, col_ref2 = st.columns(2)
        with col_ref1:
            st.markdown("""
            | Superfície Urbana | C |
            |-------------------|---|
            | Telhados impermeáveis | 0,75 – 0,95 |
            | Calçadas / asfalto | 0,70 – 0,95 |
            | Paralelepípedo | 0,70 – 0,85 |
            | Residencial denso | 0,60 – 0,80 |
            | Residencial baixa dens. | 0,25 – 0,40 |
            | Parques / jardins | 0,10 – 0,35 |
            """)
        with col_ref2:
            st.markdown("""
            | Superfície Rural | C |
            |------------------|---|
            | Floresta densa | 0,10 – 0,25 |
            | Capoeira / mata secundária | 0,20 – 0,35 |
            | Pastagem bem coberta | 0,25 – 0,45 |
            | Culturas em fileiras | 0,40 – 0,60 |
            | Solo exposto (lavrado) | 0,50 – 0,70 |
            """)

    # ── ABA 4 — RESULTADOS ───────────────────────────────────────────────
    with tab_result:
        st.markdown("### Resultados — Vazão Máxima pelo Método Racional")

        # ── Recalcular tudo com os valores atuais do session_state ──────
        tc_min_r = calc_tc_kirpich(st.session_state["L_m"], st.session_state["S"])
        i_r = calc_idf(
            st.session_state["K"], st.session_state["a_idf"],
            st.session_state["T_anos"], tc_min_r,
            st.session_state["b_idf"], st.session_state["c_idf"],
        )
        C_med_r = calc_C_medio(
            st.session_state["pct_urban"],
            st.session_state["C_urb"],
            st.session_state["C_rur"],
        )
        Q_atual = calc_Q_racional(C_med_r, i_r, st.session_state["area_km2"])

        # Cenário hipotético: 80% urbano
        C_hip = calc_C_medio(80, st.session_state["C_urb"], st.session_state["C_rur"])
        Q_hip = calc_Q_racional(C_hip, i_r, st.session_state["area_km2"])

        # Cenário natural: 0% urbano
        C_nat = calc_C_medio(0, st.session_state["C_urb"], st.session_state["C_rur"])
        Q_nat = calc_Q_racional(C_nat, i_r, st.session_state["area_km2"])

        # ── Painel de destaque ─────────────────────────────────────────
        st.markdown(f"""
        <div class="result-box">
            <div class="label">Vazão Máxima de Projeto — Método Racional</div>
            <div class="value">{Q_atual:.3f}<span class="unit">m³/s</span></div>
            <div style="margin-top:10px; font-size:13px; opacity:0.85;">
                Tr = {st.session_state['T_anos']} anos &nbsp;|&nbsp;
                C = {C_med_r:.3f} &nbsp;|&nbsp;
                i = {i_r:.2f} mm/h &nbsp;|&nbsp;
                A = {st.session_state['area_km2']:.2f} km²
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Métricas comparativas ─────────────────────────────────────
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric(
            "🌿 Cenário Natural (0% urbano)",
            f"{Q_nat:.3f} m³/s",
            help="Bacia completamente rural/florestal.",
        )
        col_m2.metric(
            f"🏘️ Cenário Atual ({st.session_state['pct_urban']}% urbano)",
            f"{Q_atual:.3f} m³/s",
            delta=f"+{((Q_atual/Q_nat - 1)*100):.1f}% vs natural" if Q_nat > 0 else "",
        )
        col_m3.metric(
            "🏙️ Cenário Hipotético (80% urbano)",
            f"{Q_hip:.3f} m³/s",
            delta=f"+{((Q_hip/Q_nat - 1)*100):.1f}% vs natural" if Q_nat > 0 else "",
            delta_color="inverse",
        )

        # ── Gráfico de barras comparativo ─────────────────────────────
        st.markdown('<div class="section-divider"><hr/><span>Comparativo de Vazões por Grau de Urbanização</span><hr/></div>',
                    unsafe_allow_html=True)

        # Barras para múltiplos cenários
        pcts  = list(range(0, 101, 10))
        Qs    = [calc_Q_racional(
                    calc_C_medio(p, st.session_state["C_urb"], st.session_state["C_rur"]),
                    i_r, st.session_state["area_km2"]
                 ) for p in pcts]
        cores_barras = [
            ACCENT if p == st.session_state["pct_urban"] else
            ("#f59e0b" if p == 80 else "#bae6fd")
            for p in pcts
        ]

        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            x=[f"{p}%" for p in pcts],
            y=Qs,
            marker_color=cores_barras,
            marker_line_color="white",
            marker_line_width=1.5,
            name="Q máximo",
            hovertemplate="Urbano: %{x}<br>Q = %{y:.3f} m³/s<extra></extra>",
        ))

        # Anotação no cenário atual
        fig_bar.add_annotation(
            x=f"{st.session_state['pct_urban']}%",
            y=Q_atual,
            text=f"Cenário<br>atual<br>{Q_atual:.3f} m³/s",
            showarrow=True, arrowhead=2, arrowcolor=ACCENT,
            font=dict(size=11, color=ACCENT_D), bgcolor="white",
            bordercolor=ACCENT, borderwidth=1, borderpad=4,
            ay=-50,
        )
        fig_bar.add_annotation(
            x="80%",
            y=Q_hip,
            text=f"80% urbano<br>{Q_hip:.3f} m³/s",
            showarrow=True, arrowhead=2, arrowcolor=WARNING,
            font=dict(size=11, color="#92400e"), bgcolor="white",
            bordercolor=WARNING, borderwidth=1, borderpad=4,
            ay=-50,
        )

        fig_bar.update_layout(
            **plotly_config(),
            title=dict(
                text=f"Vazão Máxima Q (m³/s) × Grau de Urbanização — Tr = {st.session_state['T_anos']} anos",
                font=dict(size=14, weight="bold"),
            ),
            xaxis=dict(title="Percentagem de Área Urbanizada", gridcolor="#e2e8f0"),
            yaxis=dict(title="Vazão Máxima Q (m³/s)", gridcolor="#e2e8f0"),
            height=400,
            showlegend=False,
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        if Q_nat > 0:
            variacao = (Q_hip / Q_nat - 1) * 100
            st.markdown(f"""
            <div class="alert-warning">
            <b>📈 Impacto da Urbanização:</b> A passagem de uma bacia
            <b>100% natural</b> para <b>80% urbanizada</b> provoca um aumento de
            <b>{variacao:.1f}%</b> na vazão máxima de pico — de {Q_nat:.3f} m³/s
            para {Q_hip:.3f} m³/s — mantendo a mesma chuva de projeto.
            Este é o efeito da redução do coeficiente de infiltração e da eliminação
            da interceptação vegetal.
            </div>
            """, unsafe_allow_html=True)

        # ── Memória de Cálculo (expander) ──────────────────────────────
        with st.expander("📖 Mostrar Resolução Passo a Passo"):
            st.markdown("#### Memória de Cálculo — Método Racional")
            st.markdown("---")

            # PASSO 1
            st.markdown('<div class="step-box">', unsafe_allow_html=True)
            st.markdown('<div class="step-title">Passo 1 — Tempo de Concentração (Kirpich)</div>',
                        unsafe_allow_html=True)
            st.markdown("**Equação:**")
            st.latex(r"t_c = 0{,}0195 \cdot \frac{L^{0,77}}{S^{0,385}}")
            st.markdown("**Substituindo os valores:**")
            st.latex(
                rf"t_c = 0{{,}}0195 \cdot \frac{{{st.session_state['L_m']:.1f}^{{0,77}}}}"
                rf"{{{st.session_state['S']:.4f}^{{0,385}}}}"
            )
            st.latex(
                rf"t_c = 0{{,}}0195 \cdot \frac{{{st.session_state['L_m'] ** 0.77:.4f}}}"
                rf"{{{st.session_state['S'] ** 0.385:.4f}}}"
            )
            st.latex(rf"t_c = {tc_min_r:.4f} \text{{ min}} \approx {tc_min_r:.2f} \text{{ min}}")
            st.markdown('</div>', unsafe_allow_html=True)

            # PASSO 2
            st.markdown('<div class="step-box">', unsafe_allow_html=True)
            st.markdown('<div class="step-title">Passo 2 — Intensidade de Chuva (Equação IDF)</div>',
                        unsafe_allow_html=True)
            st.markdown("**Equação:**")
            st.latex(r"i = \frac{K \cdot T^a}{(t_c + b)^c}")
            st.markdown("**Substituindo os valores:**")
            st.latex(
                rf"i = \frac{{{st.session_state['K']:.2f} \cdot {st.session_state['T_anos']}^{{{st.session_state['a_idf']:.3f}}}}}"
                rf"{{({tc_min_r:.2f} + {st.session_state['b_idf']:.1f})^{{{st.session_state['c_idf']:.3f}}}}}"
            )
            st.latex(
                rf"i = \frac{{{st.session_state['K']:.2f} \cdot {st.session_state['T_anos'] ** st.session_state['a_idf']:.4f}}}"
                rf"{{{(tc_min_r + st.session_state['b_idf']) ** st.session_state['c_idf']:.4f}}}"
            )
            st.latex(rf"i = {i_r:.4f} \text{{ mm/h}}")
            st.markdown('</div>', unsafe_allow_html=True)

            # PASSO 3
            st.markdown('<div class="step-box">', unsafe_allow_html=True)
            st.markdown('<div class="step-title">Passo 3 — Coeficiente de Escoamento Médio</div>',
                        unsafe_allow_html=True)
            f_urb = st.session_state["pct_urban"] / 100.0
            f_rur = 1.0 - f_urb
            st.markdown("**Equação:**")
            st.latex(r"C_{médio} = C_{urb} \cdot f_{urb} + C_{rur} \cdot f_{rur}")
            st.markdown("**Substituindo:**")
            st.latex(
                rf"C_{{médio}} = {st.session_state['C_urb']:.2f} \cdot {f_urb:.2f}"
                rf" + {st.session_state['C_rur']:.2f} \cdot {f_rur:.2f}"
            )
            st.latex(
                rf"C_{{médio}} = {st.session_state['C_urb'] * f_urb:.4f}"
                rf" + {st.session_state['C_rur'] * f_rur:.4f}"
            )
            st.latex(rf"C_{{médio}} = {C_med_r:.4f}")
            st.markdown('</div>', unsafe_allow_html=True)

            # PASSO 4
            st.markdown('<div class="step-box">', unsafe_allow_html=True)
            st.markdown('<div class="step-title">Passo 4 — Vazão Máxima (Método Racional)</div>',
                        unsafe_allow_html=True)
            st.markdown("**Equação geral:**")
            st.latex(
                r"Q = \frac{C_{médio} \cdot i \cdot A}{3{,}6} "
                r"\quad [m^3/s] \quad \leftarrow A \text{ em km}^2, \; i \text{ em mm/h}"
            )
            st.markdown("**Demonstração da conversão de unidades:**")
            st.latex(
                r"Q \left[\frac{m^3}{s}\right] = "
                r"C \cdot i \left[\frac{mm}{h}\right] \cdot A \left[km^2\right] \cdot "
                r"\frac{1000 \, m/km^2}{3600 \, s/h} = "
                r"\frac{C \cdot i \cdot A}{3{,}6}"
            )
            st.markdown("**Substituindo os valores:**")
            st.latex(
                rf"Q = \frac{{{C_med_r:.4f} \times {i_r:.4f} \times {st.session_state['area_km2']:.2f}}}{{3{{,}}6}}"
            )
            st.latex(
                rf"Q = \frac{{{C_med_r * i_r * st.session_state['area_km2']:.6f}}}{{3{{,}}6}}"
            )
            st.latex(rf"\boxed{{Q = {Q_atual:.4f} \; m^3/s}}")
            st.markdown('</div>', unsafe_allow_html=True)

            st.success(
                f"✅ **Resultado Final:** Q = **{Q_atual:.4f} m³/s** "
                f"≈ **{Q_atual * 1000:.2f} L/s** "
                f"para Tr = {st.session_state['T_anos']} anos."
            )


# ──────────────────────────────────────────────────────────────────────────────
# ROTEADOR PRINCIPAL
# ──────────────────────────────────────────────────────────────────────────────
if st.session_state.get("pagina_ativa", "estudo") == "estudo":
    render_page_estudo()
else:
    render_page_simulador()
