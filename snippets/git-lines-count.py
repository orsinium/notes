import plotnine as gg
import pandas
import subprocess

# collect all merge commits
res = subprocess.run(['git', 'rev-list', '--merges', 'HEAD'], stdout=subprocess.PIPE)
commits = res.stdout.decode().split()

# collect inerted and deleted lines count
sizes = []
for sha1, sha2 in zip(commits, commits[1:]):
    res = subprocess.run(['git', 'diff', '--shortstat', sha1, sha2], stdout=subprocess.PIPE)
    words = res.stdout.decode().split()
    plus = 0
    minus = 0
    for i, word in enumerate(words):
        if 'insertion' in word:
            plus = int(words[i-1])
        if 'deletion' in word:
            minus = int(words[i-1])
    sizes.append({'insertions': plus, 'deletions': minus})


df = pandas.DataFrame(sizes)
df['newlines'] = df.insertions - df.deletions
df.describe()


# show some basic stat
for n in (-500, -100):
    rat = df[df.newlines < n].size / df.size
    print('<', n, round(rat * 100, 2), '%')
for n in (0, 100, 500, 1000, 2000):
    rat = df[df.newlines > n].size / df.size
    print('>', n, round(rat * 100, 2), '%')


# draw charts
(
    gg.ggplot(df, gg.aes(x='newlines'))
    + gg.geom_density()
    + gg.xlim(-2000, 0)
)

(
    gg.ggplot(df, gg.aes(x='newlines'))
    + gg.geom_density()
    + gg.xlim(0, 2000)
)
