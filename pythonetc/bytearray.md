# bytearray

Published: 09 March 2021, 18:00

Types `str` and `bytes` are immutable. As we learned in previous posts, `+` is optimized for `str` but sometimes you need a fairly mutable type. For such cases, there is `bytearray` type. It is a "hybrid" of `bytes` and `list`:

```python
b = bytearray(b'hello, ')
b.extend(b'@pythonetc')
b
# bytearray(b'hello, @pythonetc')

b.upper()
# bytearray(b'HELLO, @PYTHONETC')
```

The type `bytearray` has all methods of both `bytes` and `list` except `sort`:

```python
set(dir(bytearray)) ^ (set(dir(bytes)) | set(dir(list)))
# {'__alloc__', '__class_getitem__', '__getnewargs__', '__reversed__', 'sort'}
```

If you're looking for reasons why there is no `bytearray.sort`, there is the only answer we found: [stackoverflow.com/a/22783330/8704691](https://stackoverflow.com/a/22783330/8704691).
