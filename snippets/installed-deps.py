"""
The script uses dephell to analyze installed dependencies
and find how many times a dependency is used in another dependency.

For example, `('dephell', 25)` means that there are 25 packages
installed that use dephell.
"""

from collections import Counter

from dephell.config import config
from dephell.controllers import analyze_conflict
from dephell.converters import InstalledConverter
from dephell.exceptions import ExtraException


# black has no releases not markerd as pre-release.
config.attach(dict(prereleases=True))

# read deps
resolver = InstalledConverter().load_resolver(None)

# build dependencies tree
try:
    resolved = resolver.resolve()
except ExtraException as e:
    print(str(e), e.extra)
    exit(1)
if not resolved:
    print('cannot resolve')
    print(analyze_conflict(resolver=resolver))
    exit(2)

# get most used dependencies
c = Counter()
for dep in resolver.graph:
    for source in dep.constraint.sources:
        c[source] += 1
print(*c.most_common(20)[1:], sep='\n')
