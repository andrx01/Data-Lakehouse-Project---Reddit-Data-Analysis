import os
import pandas as pd
import re
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from langdetect import detect
from pathlib import Path

PROJECT_PATH = Path(__file__).resolve().parents[2]

raw_path = PROJECT_PATH / "data" / "raw" / "reddit_posts.csv"
silver_path = PROJECT_PATH / "data" / "silver" / "reddit_posts_clean.csv"
model_path = PROJECT_PATH / "models" / "relevance_model.pkl"

print("📥 Carregando dados RAW...")
print(f"🔎 Procurando arquivo em: {raw_path}")

if not raw_path.exists():
    raise FileNotFoundError(f"❌ Arquivo RAW não encontrado: {raw_path}")

df = pd.read_csv(raw_path)

def limpar_texto(texto):
    if not isinstance(texto, str):
        return ""
    texto = texto.lower()
    texto = re.sub(r"http\S+|www\S+|https\S+", "", texto)
    texto = re.sub(r"[^\w\s]", "", texto)
    texto = re.sub(r"\d+", "", texto)
    return texto.strip()

def detectar_idioma(texto):
    try:
        return detect(texto)
    except:
        return "unknown"

# Ajuste: trata ausência de 'selftext'
if 'selftext' in df.columns:
    df['clean_text'] = df['title'].fillna('') + ' ' + df['selftext'].fillna('')
else:
    df['clean_text'] = df['title'].fillna('')

df['clean_text'] = df['clean_text'].apply(limpar_texto)
df['language'] = df['clean_text'].apply(detectar_idioma)

df = df[df['language'].isin(['pt', 'en'])]

if not model_path.exists():
    print("🛠️ Treinando modelo de relevância...")
    vectorizer = TfidfVectorizer(max_features=500)
    X = vectorizer.fit_transform(df['clean_text'])
    y = (df['score'] > df['score'].median()).astype(int)
    
    model = LogisticRegression()
    model.fit(X, y)
    
    os.makedirs(model_path.parent, exist_ok=True)
    joblib.dump((vectorizer, model), model_path)
else:
    print("✅ Carregando modelo existente...")
    vectorizer, model = joblib.load(model_path)

print("🤖 Classificando relevância...")
X = vectorizer.transform(df['clean_text'])
df['relevance'] = model.predict(X)

df_relevant = df[df['relevance'] == 1]

os.makedirs(silver_path.parent, exist_ok=True)
df_relevant.to_csv(silver_path, index=False)
print(f"✅ Dados tratados salvos em {silver_path} ({len(df_relevant)} registros)")
