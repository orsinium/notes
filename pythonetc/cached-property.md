# @cached_property

Published: 16 July 2020, 18:00

Decorator `@cached_property` is an amazing way to simplify your code. It's like the regular `@property` but remembers the value after the first call:

```python
class C:
  @cached_property
  def p(self):
    print('computing...')
    return 1

c = C()
c.p
# computing...
# 1

c.p
# 1
```

The implementation is short and relatively simple:

```python
class cached_property:
  def __init__(self, func):
    self.func = func

  def __get__(self, obj, cls):
    if obj is None:
        return self
    value = obj.__dict__[self.func.__name__] = self.func(obj)
    return value
```

However, there are a few corner-cases, like async functions and threads. Luckily, from Python 3.8 it's a part of standard library ([functools.cached_property](https://docs.python.org/dev/library/functools.html#functools.cached_property)) and for older versions [cached-propery](https://github.com/pydanny/cached-property) library can be used.
