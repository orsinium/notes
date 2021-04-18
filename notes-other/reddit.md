# Analyzing reddit posts

```bash
wget https://files.pushshift.io/reddit/submissions/RS_2020-03.zst
```

```python
from datetime import datetime
import json
import io

import pandas
import zstandard
import plotnine as gg
from tqdm import tqdm
```

```python
paths = [
    '/home/gram/Downloads/RS_2020-02.zst',
    '/home/gram/Downloads/RS_2020-03.zst',
]
subreddits = {'python', 'golang', 'coolgithubprojects', 'madeinpython', 'datascience'}
posts = []
for path in paths:
    with open(path, 'rb') as fh:
        dctx = zstandard.ZstdDecompressor()
        stream_reader = dctx.stream_reader(fh)
        text_stream = io.TextIOWrapper(stream_reader, encoding='utf-8')
        for line in tqdm(text_stream):
            post = json.loads(line)
            if post['subreddit'].lower() not in subreddits:
                continue
            posts.append((
                datetime.fromtimestamp(post['created_utc']),
                post['domain'],
                post['num_comments'],
                post['id'],
                post['score'],
                post['subreddit'],
                post['title'],
            ))
```

```python
df = pandas.DataFrame(posts, columns=['created', 'domain', 'comments', 'id', 'score', 'subreddit', 'title'])
df.head()
```

```python
df.to_pickle('filtered.bin')
df = pandas.read_pickle('filtered.bin')
```

```python
threshold = 5
subreddit = 'python'
```

```python
(df.score > threshold).mean()
```

```python
df2 = df[df.subreddit.str.lower() == subreddit.lower()]
df2 = pandas.DataFrame(dict(
    hour=df2.created.apply(lambda x: x.hour),
    survived=df2.score > threshold,
))
df2 = df2.groupby(['hour'], as_index=False)
df2 = pandas.DataFrame(dict(
    hour=range(24),
    survived=df2.survived.sum().survived,
    total=df2.count().survived,
))
```

```python
(
    gg.ggplot(df2)
    + gg.theme_light()
    + gg.geom_col(gg.aes(x='hour', y='total', fill='"#3498db"'))
    + gg.geom_col(gg.aes(x='hour', y='survived', fill='"#c0392b"'))
    + gg.scale_fill_manual(name=f'rating >{threshold}' , guide='legend', values=['#3498db', '#c0392b'], labels=['no', 'yes'])
    + gg.xlab('hour (UTC)')
    + gg.ylab('posts')
    + gg.ggtitle(f'Posts in /r/{subreddit} per hour\nand how many got rating above {threshold}')
)
```

```python
(
    gg.ggplot(df2)
    + gg.theme_light()
    + gg.geom_col(gg.aes(x='hour', y=f'survived / total * 100'), fill="#c0392b")
    + gg.geom_text(
        gg.aes(x='hour', y=1, label='survived / total * 100'),
        va='bottom', ha='center', angle=90, format_string='{:.0f}%', color='white',
    )
    + gg.xlab('hour (UTC)')
    + gg.ylab(f'% of posts with rating >{threshold}')
    + gg.ylim(0, 100)
    + gg.ggtitle(f'Posts in /r/{subreddit} with rating >{threshold} per hour')
)
```
