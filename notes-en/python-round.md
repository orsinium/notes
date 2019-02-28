`round` function rounds a number to a given precision in decimal digits.

```
>>> round(1.2)
1
>>> round(1.8)
2
>>> round(1.228, 1)
1.2
```

Also you can set up negative precision:

```
>>> round(413.77, -1)
410.0
>>> round(413.77, -2)
400.0
```

`round` returns value of type of input number:

```
>>> type(round(2, 1))
<class 'int'>

>>> type(round(2.0, 1))
<class 'float'>

>>> type(round(Decimal(2), 1))
<class 'decimal.Decimal'>

>>> type(round(Fraction(2), 1))
<class 'fractions.Fraction'>
```


For your own classes you can define `round` processing with `__round__` method:

```
>>> class Number(int):
...   def __round__(self, p=-1000):
...     return p
...
>>> round(Number(2))
-1000
>>> round(Number(2), -2)
-2
```

Values are rounded to the closest multiple of 10 to the power minus ndigits. If two multiples are equally close, rounding is done toward the even choice:

```
>>> round(0.5)
0
>>> round(1.5)
2
```

Sometimes rounding of floats can be a little bit surprising:

```
>>> round(2.85, 1)
2.9
```

This is because most decimal fractions [can't be represented exactly as a float](https://docs.python.org/3.7/tutorial/floatingpoint.html):

```
>>> format(2.85, '.64f')
'2.8500000000000000888178419700125232338905334472656250000000000000'
```

If you want to round half up you can use `decimal.Decimal`:

```
>>> from decimal import Decimal, ROUND_HALF_UP
>>> Decimal(1.5).quantize(0, ROUND_HALF_UP)
Decimal('2')
>>> Decimal(2.85).quantize(Decimal('1.0'), ROUND_HALF_UP)
Decimal('2.9')
>>> Decimal(2.84).quantize(Decimal('1.0'), ROUND_HALF_UP)
Decimal('2.8')
```
