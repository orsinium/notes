# Everything about Counter

I think, `collections.Counter` is the most magic and powerful container in Python. This is smart and beautiful [multiset](https://en.wikipedia.org/wiki/Multiset) realization. Let's have a look at what `Counter` can do.

## Basic usage

Basic usage for Counter is to count some element (for example, words) in a sequence and get N most popular.

```python
from collections import Counter

words = 'to be or not to be'.split()

c = Counter(words)
# Counter({'to': 2, 'be': 2, 'or': 1, 'not': 1})

c.most_common()
# [('to', 2), ('be', 2), ('or', 1), ('not', 1)]

c.most_common(3)
# [('to', 2), ('be', 2), ('or', 1)]
```

Ok, now let's dive into Counter features.

## Init

`Counter` is a child of `dict`, and all elements, so you can initialize it from a sequence as in "Basic usage" section or by any way how you initialize `dict`.

```python
Counter()
Counter('gallahad')
Counter({'a': 4, 'b': 2})
Counter(a=4, b=2)
Counter({1: 2, 3: 4})
```

You can use any `int` as value. Yes, zero or negative too.

## Manage values

You can get, set and delete values from Counter:

```python
c = Counter(first=2, second=3)
c['junk'] = 4
c  # Counter({'first': 2, 'second': 3, 'junk': 4})
c['junk']
del c['junk']
c  # Counter({'first': 2, 'second': 3})
```

## Default value

If you try to get missing value Counter returns 0 instead of raising `KeyError`:

```python
c['missing']
# 0
```

It allows you to work with `Counter` as with `defaultdict(int)`.

Use `in` if you want to check that a Counter contains a key:

```python
'missing' in c
# False

'first' in c
# True
```

## Dict

Counter has all dict methods:

```python
list(c.items())
# [('first', 2), ('second', 3)]

list(c.keys())
# ['first', 'second']

list(c.values())
# [2, 3]
```

Method `.update()` smarter than in `dict` and can get anything that you can pass in `init`. Also, it merges values.

```python
c = Counter({'first': 1})
c.update(Counter({'second': 2}))
c.update({'third': 3})
c.update(fourth=5)
c.update(fourth=-1)
c.update(['fifth'] * 6)
c
# Counter({'first': 1, 'second': 2, 'third': 3, 'fourth': 4, 'fifth': 6})
```

## Arithmetic operations

```python
c1 = Counter(first=1, common=2)
c2 = Counter(common=3, second=4)

c1 + c2
# Counter({'first': 1, 'common': 5, 'second': 4})

c1 - c2
# Counter({'first': 1})

c2 - c1
# Counter({'common': 1, 'second': 4})
```

As you can see, arithmetic operations drop negative values.

```python
Counter(a=-2) - Counter(a=-1)
# Counter()

Counter(a=-2) + Counter(a=-1)
# Counter()
```

## Set operations

Counter supports set operations:

```python
c1 = Counter(first=1, common=2)
c2 = Counter(common=3, second=4)

c1 & c2
# Counter({'common': 2})

c2 & c1
# Counter({'common': 2})

c1 | c2
# Counter({'first': 1, 'common': 3, 'second': 4})

c2 | c1
# Counter({'common': 3, 'second': 4, 'first': 1})
```

Union (`|`)

This operations also drop non-positive values:

```python
Counter(a=-1) | Counter(b=-2)
# Counter()
```

## A little bit more about non-positive values

From source code:

```python
# Outputs guaranteed to only include positive counts.
# To strip negative and zero counts, add-in an empty counter:
c += Counter()
```

You can use this magic to drop or flip negative values:

```python
+Counter(a=-1)
# Counter()

+Counter(a=1)
# Counter({'a': 1})

-Counter(a=-1)
# Counter({'a': 1})

-Counter(a=1)
# Counter()
```

## Get elements

Some ways to get elements from Counter:

```python
c = Counter(first=1, second=2, third=3)

list(c.items())
# [('first', 1), ('second', 2), ('third', 3)]

# iterator over elements repeating each as many times as its count
list(c.elements())
# ['first', 'second', 'second', 'third', 'third', 'third']

c.most_common()
# [('third', 3), ('second', 2), ('first', 1)]

c.most_common(2)
# [('third', 3), ('second', 2)]
```

## Conclusion

`Counter` is:

* Dictionary with a default value,
* Supports set and arithmetic operations,
* Can count elements in sequence fast because of C realization of this function,
* Can return N or all elements sorted by value,
* Can merge 2 or more Counters,
* Drops negative values.

That's beautiful, isn't it?
