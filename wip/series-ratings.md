# Ratings of TV series

[public IMDB dataset](https://www.imdb.com/interfaces/).

Read datasets:

```python
import pandas

meta = pandas.read_csv('./title.basics.tsv.gz', sep='\t', low_memory=False)
eps = pandas.read_csv(
    './title.episode.tsv.gz',
    sep='\t',
    dtype=dict(seasonNumber='Int64', episodeNumber='Int64'),
    na_values=r'\N',
)
ratings = pandas.read_csv('./title.ratings.tsv.gz', sep='\t')
```

Create a new dataset:

```python
df1 = pandas.DataFrame()
df1['uid'] = meta.tconst
df1['title'] = meta.primaryTitle
df1.set_index('uid', inplace=True)
```

## The first episode

Insert for each series the first episode UID:

```python
# filter
first_eps = eps[(eps.seasonNumber == 1) & (eps.episodeNumber == 1)]
# join
df2 = df1.join(first_eps.set_index('parentTconst'), how='inner')
# cleanup
del df2['seasonNumber']
del df2['episodeNumber']
df2.rename(columns={'tconst': 'first_uid'}, inplace=True)
```

Insert for each series the first episode rating and number of votes:

```python
# join
df3 = df2.join(ratings.set_index('tconst'), on='first_uid', how='inner')
# cleanup
df3.rename(columns={'averageRating': 'first_rating', 'numVotes': 'first_votes'}, inplace=True)
```

Show the most popular first episodes:

```python
df3.sort_values('first_votes', ascending=False)
```

## The last episode

Find the last season number:

```python
last_seasons = eps.groupby('parentTconst').max()
last_seasons = last_seasons.loc[eps.parentTconst].seasonNumber.to_numpy()
last_seasons = pandas.Series(last_seasons).astype('Int64')
```

Knowing the last season, we can filter only apisodes in the last season, and find th last episode in each:

```python
last_eps = eps[eps.seasonNumber == last_seasons].groupby('parentTconst').max()
```

```python
# join
df4 = df3.join(last_eps, how='inner')
# cleanup
df4.rename(columns={'tconst': 'last_uid', 'seasonNumber': 'last_season', 'episodeNumber': 'last_episode'}, inplace=True)
```

```python
# join
df5 = df4.join(ratings.set_index('tconst'), on='last_uid', how='inner')
# cleanup
df5.rename(columns={'averageRating': 'last_rating', 'numVotes': 'last_votes'}, inplace=True)
```

```python
df5.sort_values('last_votes', ascending=False)
```

## Stats

```python
df6 = df5[df5.first_votes > 1000]
```

```python
df7 = df6.copy()
df7['votes_ratio'] = df7.last_votes / df7.first_votes
df7['rating_ratio'] = df7.last_rating / df7.first_rating
```

```python
df7.sort_values('votes_ratio', ascending=False)
```

## Drawing the top

```python
import plotnine as gg
```

```python
df_plot = df.sort_values('votes_ratio', ascending=False)[:20]
# https://github.com/has2k1/plotnine/issues/295
df_plot = df_plot.assign(title=pandas.Categorical(df_plot.title, df_plot.title[::-1], ordered=True))
(
    gg.ggplot(df_plot, gg.aes(x='title'))
    + gg.geom_col(gg.aes(y='votes_ratio'))
    + gg.ylab('votes ratio (last_episode/first_episode)')
    + gg.coord_flip()
)
```

```python
df_plot = df7.sort_values('votes_ratio')[:20]
df_plot = df_plot.assign(title=pandas.Categorical(df_plot.title, df_plot.title[::-1], ordered=True))
(
    gg.ggplot(df_plot, gg.aes(x='title'))
    + gg.geom_col(gg.aes(y='1/votes_ratio'))
    + gg.ylab('votes ratio (first_episode/last_episode), log10 scale')
    + gg.scale_y_log10()
    + gg.coord_flip()
)
```

```python
title = 'game of thrones'
matches = meta[(meta.originalTitle.str.lower() == title.lower()) & (meta.titleType == 'tvSeries')]
series_uid = matches.iloc[0].tconst
f'https://www.imdb.com/title/{series_uid}'
```

```python
episodes = eps[eps.parentTconst == series_uid]
episodes = episodes.set_index('tconst').join(ratings.set_index('tconst'), how='inner')
episodes['position'] = range(len(episodes))
```

```python
(
    gg.ggplot(episodes.reset_index(), gg.aes(x='position', y='numVotes'))
    + gg.geom_line()
    + gg.geom_point(gg.aes(color='averageRating'))
    + gg.xlab('episodes')
    + gg.ylab('votes')
)
```
