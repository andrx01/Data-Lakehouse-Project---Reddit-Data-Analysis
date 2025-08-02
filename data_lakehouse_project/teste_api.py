import praw
import yaml

# Agora o caminho é direto
with open('configs/config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

reddit = praw.Reddit(
    client_id=config['reddit']['client_id'],
    client_secret=config['reddit']['client_secret'],
    user_agent=config['reddit']['user_agent']
)

print("Conexão OK:", reddit.read_only)

subreddit_name = config['reddit']['subreddits'][0]
print(f"\nPosts recentes em r/{subreddit_name}:")
for post in reddit.subreddit(subreddit_name).hot(limit=5):
    print("-", post.title)