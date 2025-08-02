import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter
import re

# Detectar raiz do projeto
PROJECT_PATH = Path(__file__).resolve().parents[2]
silver_path = PROJECT_PATH / "data" / "silver" / "reddit_posts_clean.csv"
gold_dir = PROJECT_PATH / "data" / "gold"
os.makedirs(gold_dir, exist_ok=True)

# Carregar dados Silver

print("📥 Carregando dados Silver...")
df = pd.read_csv(silver_path)

# Verifica se 'clean_text' existe
if 'clean_text' not in df.columns:
    if 'title' in df.columns:
        df['clean_text'] = df['title'].fillna('')
    else:
        raise KeyError("Nenhuma coluna de texto encontrada para análise.")


# Estatísticas básicas
posts_count = df.groupby('subreddit').size().reset_index(name='num_posts')
posts_count.to_csv(gold_dir / 'posts_count.csv', index=False)

top_posts = df.sort_values(by='score', ascending=False).head(20)
top_posts.to_csv(gold_dir / 'top_posts.csv', index=False)

engagement_avg = df.groupby('subreddit').agg({
    'score': 'mean',
    'num_comments': 'mean'
}).reset_index()
engagement_avg.rename(columns={'score': 'avg_score', 'num_comments': 'avg_comments'}, inplace=True)
engagement_avg.to_csv(gold_dir / 'engagement_avg.csv', index=False)

# Evolução temporal
df['created_datetime'] = pd.to_datetime(df['created_utc'], unit='s')
df['month'] = df['created_datetime'].dt.to_period('M')
monthly_posts = df.groupby('month').size().reset_index(name='num_posts')
monthly_posts['month'] = monthly_posts['month'].astype(str)  # ✅ Fix do erro
monthly_posts.to_csv(gold_dir / 'posts_by_month.csv', index=False)

# Autores mais ativos

if 'author' in df.columns:
    top_authors = df.groupby('author').agg({'score': 'sum', 'id': 'count'}) \
                    .rename(columns={'id': 'num_posts'}) \
                    .reset_index() \
                    .sort_values(by='num_posts', ascending=False).head(20)
    top_authors.to_csv(gold_dir / 'top_authors.csv', index=False)

# Palavras e Bigramas
text_data = " ".join(df['clean_text'].astype(str).tolist()).lower()
tokens = re.findall(r'\b\w+\b', text_data)

stopwords = set([
    'a','o','e','de','do','da','em','no','na','para','com',
    'um','uma','que','os','as','por','mais','sobre','this','that','and','the','for'
])
filtered_tokens = [word for word in tokens if word not in stopwords and len(word) > 3]
word_counts = Counter(filtered_tokens)
common_words = pd.DataFrame(word_counts.most_common(30), columns=['word', 'count'])
common_words.to_csv(gold_dir / 'common_words.csv', index=False)

vectorizer = CountVectorizer(ngram_range=(2, 2), stop_words=list(stopwords))
X = vectorizer.fit_transform(df['clean_text'].astype(str))
bigram_counts = sorted(zip(vectorizer.get_feature_names_out(), X.toarray().sum(axis=0)), key=lambda x: -x[1])
bigrams_df = pd.DataFrame(bigram_counts, columns=['bigram', 'count']).head(30)
bigrams_df.to_csv(gold_dir / 'bigrams.csv', index=False)

# Visualizações
sns.set(style="whitegrid")

# Posts por subreddit
plt.figure(figsize=(10, 5))
sns.barplot(data=posts_count, x='subreddit', y='num_posts')
plt.title('Quantidade de Posts por Subreddit')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(gold_dir / 'posts_by_subreddit.png')
plt.close()

# Engajamento médio
plt.figure(figsize=(10, 5))
sns.barplot(data=engagement_avg, x='subreddit', y='avg_score')
plt.title('Engajamento Médio (Score) por Subreddit')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(gold_dir / 'engagement_avg.png')
plt.close()

# Evolução temporal
plt.figure(figsize=(12, 6))
sns.lineplot(data=monthly_posts, x='month', y='num_posts', marker='o')
plt.title('Posts ao longo do tempo')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(gold_dir / 'monthly_engagement.png')
plt.close()

# Palavras mais comuns
plt.figure(figsize=(10, 6))
sns.barplot(data=common_words.head(20), x='count', y='word')
plt.title('Top 20 Palavras Mais Frequentes')
plt.tight_layout()
plt.savefig(gold_dir / 'common_words.png')
plt.close()

# Bigramas
plt.figure(figsize=(10, 6))
sns.barplot(data=bigrams_df.head(20), x='count', y='bigram')
plt.title('Top 20 Bigramas')
plt.tight_layout()
plt.savefig(gold_dir / 'bigrams.png')
plt.close()

# WordCloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(" ".join(filtered_tokens))
plt.figure(figsize=(12, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('WordCloud - Palavras Relevantes')
plt.tight_layout()
plt.savefig(gold_dir / 'wordcloud.png')
plt.close()

print(f"✅ Camada Gold criada com sucesso em: {gold_dir}")
print("Arquivos gerados:")
for file in os.listdir(gold_dir):
    print(" -", file)
