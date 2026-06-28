# 💧 HydroCalc Paraná

**Ferramenta Didática Interativa — Hidrologia de Bacias e Método Racional**

Estudo de caso: Região de Foz do Iguaçu / Cascavel — PR

---

## Sobre a Aplicação

O **HydroCalc Paraná** é uma ferramenta pedagógica desenvolvida em Python com Streamlit para apoiar o ensino de hidrologia aplicada. Ela permite:

- 🗺️ **Conhecer** a Bacia Hidrográfica do Rio Paraná e seu comportamento climático e de uso do solo.
- 📐 **Simular** de forma interativa a vazão máxima pelo **Método Racional**, com:
  - Cálculo do Tempo de Concentração (fórmula de Kirpich)
  - Equação IDF parametrizada para Cascavel/PR (SUDERHSA)
  - Coeficiente de escoamento ponderado por tipo de uso do solo
  - Comparativo visual do impacto da urbanização na vazão de pico
  - Memória de cálculo passo a passo com equações em LaTeX

---

## Estrutura do Projeto

```
hydroCalc/
├── app.py              # Aplicação principal (único arquivo Python)
├── requirements.txt    # Dependências do projeto
└── README.md           # Este arquivo
```

---

## Execução Local

### Pré-requisitos

- Python 3.10 ou superior
- pip atualizado

### Instalação

```bash
# Clone o repositório
git clone https://github.com/<seu-usuario>/hydroCalc-parana.git
cd hydroCalc-parana

# (Recomendado) Crie um ambiente virtual
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows

# Instale as dependências
pip install -r requirements.txt
```

### Execução

```bash
streamlit run app.py
```

A aplicação abrirá automaticamente no navegador em `http://localhost:8501`.

---

## Deploy no Streamlit Community Cloud

1. **Faça o fork** deste repositório para sua conta do GitHub.

2. Acesse [share.streamlit.io](https://share.streamlit.io) e clique em **"New app"**.

3. Preencha os campos:
   - **Repository:** `<seu-usuario>/hydroCalc-parana`
   - **Branch:** `main`
   - **Main file path:** `app.py`

4. Clique em **"Deploy!"** — o Streamlit Cloud instalará as dependências automaticamente via `requirements.txt`.

5. Aguarde alguns minutos e sua aplicação estará disponível em:
   `https://<seu-usuario>-hydroCalc-parana.streamlit.app`

> **Importante:** O arquivo `requirements.txt` deve estar na **raiz do repositório**,
> no mesmo nível que `app.py`. Não é necessário `setup.py` nem `Pipfile`.

---

## Coeficientes IDF — Cascavel/PR

Os coeficientes padrão utilizados na equação IDF são derivados do ajuste estatístico
de séries pluviográficas históricas disponibilizadas pela **SUDERHSA/SIMEPAR**:

| Parâmetro | Valor default |
|-----------|--------------|
| K         | 1062,92      |
| a         | 0,141        |
| b         | 5,0          |
| c         | 0,776        |

Equação: `i = K · T^a / (tc + b)^c`  [i em mm/h, tc em min, T em anos]

Para outras cidades do Paraná, consulte o **Atlas Pluviométrico do Estado do Paraná (SUDERHSA, 2002)**.

---

## Referências Técnicas

- **Kirpich, Z.P. (1940).** Time of concentration of small agricultural watersheds. *Civil Engineering*, 10(6), 362.
- **SUDERHSA (2002).** Atlas de Recursos Hídricos do Estado do Paraná. Curitiba.
- **Porto, R.L. et al. (2012).** Hidrologia Ambiental. ABRH / EDUSP.
- **Tucci, C.E.M. (2007).** Hidrologia: Ciência e Aplicação. 4ª ed. ABRH / UFRGS.
- **DNIT (2005).** Manual de Hidrologia Básica para Estruturas de Drenagem. IPR/DNIT.

---

## Dependências

| Biblioteca | Versão mínima | Uso |
|-----------|---------------|-----|
| streamlit | 1.35.0        | Interface web interativa |
| plotly    | 5.20.0        | Gráficos interativos (IDF, barras) |

> Apenas bibliotecas Python padrão adicionalmente (math). Sem dependências de GIS, rasters ou dados externos.

---

## Licença

MIT — livre para uso acadêmico e didático.

---

*Desenvolvido para fins educacionais — PPGIES / UNILA.*
