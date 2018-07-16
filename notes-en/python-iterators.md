# About iterators and iterables

## How to create your own iterator or iterable?

In Python we have two complementary terms: iterator and iterable.

An **iterable** is an object that has an `__iter__` method which returns an iterator, or which defines a  `__getitem__` method that can take sequential indexes starting from zero (and raises an IndexError when the indexes are no longer valid). So an iterable is an object that you can get an iterator from. By default `__iter__` always returns `self`.

An **iterator** is an object with a `__next__` method.


## How to get iterator from iterable?

You can get iterator from any iterable via `iter` function:

```python
In [1]: i = iter([1, 2])

In [2]: i
Out[2]: <list_iterator at 0x7f0883065160>
```

You can iterate it manually via `next` function:

```python
In [3]: next(i)
Out[3]: 1

In [4]: next(i)
Out[4]: 2

In [5]: next(i)
StopIteration:
```

Many functions, like `map`, `functools.reduce`, `itertools.product` etc, returns iterator:

```python
In [14]: m = map(str, range(3))

In [15]: next(m)
Out[15]: '0'

In [16]: m
Out[16]: <map at 0x7f039dcc6be0>
```


## How to get iterable form iterator?

You can convert iterator to an other iterable what you want:

```python
In [23]: list(iter([1, 2, 3]))
Out[23]: [1, 2, 3]

In [24]: tuple(iter([1, 2, 3]))
Out[24]: (1, 2, 3)

In [25]: set(iter([1, 2, 3]))
Out[25]: {1, 2, 3}
```


## What about `range`?

`range` is not iterator. It is iterable:

```python
In [17]: r = range(10)

In [18]: next(r)
TypeError: 'range' object is not an iterator

In [19]: i = iter(r)

In [20]: next(i)
Out[20]: 0
```

## Why we need iterators?

Iterable, as opposite to iterator, can implements some useful methods for good performance. For example, method `__in__`for `in` operaton:

```python
In [26]: %timeit 10 ** 8 in range(10 ** 10)
623 ns ± 0.89 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)

In [27]: %timeit 10 ** 8 in iter(range(10 ** 10))
5.22 s ± 5.07 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
```



## Further reading

1. https://stackoverflow.com/questions/9884132/what-exactly-are-iterator-iterable-and-iteration
