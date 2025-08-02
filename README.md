## 📌 Visão Geral

Este projeto implementa uma arquitetura **Data Lakehouse** para coletar, processar e analisar dados do Reddit relacionados a **Análise de Dados**, **Ciência de Dados**, **Engenharia de Dados**, **Machine Learning** e temas relacionados. O pipeline é dividido em três camadas: **Bronze**, **Silver** e **Gold**, garantindo um fluxo de dados limpo, estruturado e pronto para visualização.

---

## 🏗️ Arquitetura

* **Bronze:** Coleta de dados brutos via API do Reddit.
* **Silver:** Limpeza, normalização e classificação de relevância dos posts.
* **Gold:** Agregações, métricas e visualizações finais.

📂 Estrutura de pastas:

```
data_lakehouse_project/
│── configs/
│   └── config.yaml
│── data/
│   ├── raw/          # Dados brutos
│   ├── silver/       # Dados limpos
│   └── gold/         # Métricas e gráficos finais
│── src/
│   ├── ingestion/    # Scripts de ingestão (Bronze)
│   ├── processing/   # Scripts de transformação (Silver)
│   └── analytics/    # Scripts de análise e gráficos (Gold)
│── pipeline.py        # Pipeline completo
│── requirements.txt   # Dependências do projeto
```

---

## 🚀 Execução do Pipeline Completo

Para executar todo o processo automaticamente:

```bash
python src/pipeline.py
```

🔹 Isso fará:

1. Coleta de posts do Reddit (Bronze)
2. Transformação e limpeza dos dados (Silver)
3. Geração de métricas e gráficos (Gold)

Os resultados finais estarão em:

```
data/gold/
```

---

## 📊 Visualizações Geradas

* **Wordcloud** – Principais termos
* **Top Bigramas** – Combinações de palavras mais frequentes
* **Palavras mais frequentes** – Análise de frequência
* **Posts ao longo do tempo** – Evolução temporal
* **Posts por subreddit** – Distribuição de publicações
* **Engajamento médio** – Score médio por subreddit
* **Top autores e posts** – Usuários com maior contribuição

Exemplo de gráficos:

* ![Wordcloud](data/gold/wordcloud.png)
* ![Top Bigramas](data/gold/bigrams.png)
* ![Posts por Subreddit](data/gold/posts_by_subreddit.png)

---

## ⚙️ Configuração do Projeto

1. **Instalar dependências:**

```bash
pip install -r requirements.txt
```

2. **Definir credenciais do Reddit:**

* Editar o arquivo `configs/config.yaml` com:

```yaml
reddit:
  client_id: "SEU_CLIENT_ID"
  client_secret: "SEU_SECRET"
  user_agent: "data_lakehouse_app"
```

---

## 🧠 Tecnologias Utilizadas

* Python 3.11+
* PRAW (Reddit API)
* Pandas / NumPy
* Scikit-learn (Classificação)
* Seaborn / Matplotlib / Wordcloud

