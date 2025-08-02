import praw
import yaml
import os
import pandas as pd

# Sobe dois níveis (ingestion → src → raiz)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
config_path = os.path.join(project_root, 'configs', 'config.yaml')

# Carregar config
with open(config_path, 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

reddit_config = config['reddit']
keywords = reddit_config['keywords']
post_limit = reddit_config['post_limit']

# Inicializar Reddit API
reddit = praw.Reddit(
    client_id=reddit_config['client_id'],
    client_secret=reddit_config['client_secret'],
    user_agent=reddit_config['user_agent']
)

# Coleta
data = []
for keyword in keywords:
    print(f"🔎 Coletando posts para: {keyword}")
    for post in reddit.subreddit("all").search(keyword, limit=post_limit):
        data.append({
            'id': post.id,
            'title': post.title,
            'score': post.score,
            'num_comments': post.num_comments,
            'created_utc': post.created_utc,
            'subreddit': str(post.subreddit),
            'url': post.url,
            'author': str(post.author) if post.author else "unknown",
            'keyword': keyword
        })

# Salvar camada Bronze
output_path = os.path.join(project_root, 'data', 'raw', 'reddit_posts.csv')
os.makedirs(os.path.dirname(output_path), exist_ok=True)
pd.DataFrame(data).to_csv(output_path, index=False, encoding='utf-8')

print(f"✅ Coleta concluída! Total de posts: {len(data)}")
print(f"📂 Arquivo salvo em: {output_path}")
