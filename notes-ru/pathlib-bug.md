# Баг в pathlib в Python 3.7.1

Нашли интересный баг. Когда активен [eventlet](https://github.com/eventlet/eventlet), при вызове у [pathlib.Path](https://docs.python.org/3/library/pathlib.html#pathlib.Path) метода [open](https://docs.python.org/3/library/pathlib.html#pathlib.Path.open) вылетает вот такое:

```
TypeError: open: path should be string, bytes or os.PathLike, not _NormalAccessor
```

Причину таки нашли в исходниках pathlib. В `_NormalAccessor` в качестве методов хранятся функции из модуля `os`. В python 3.6 они все оборачивались во `_wrap_strfunc`, который, помимо всего прочего оборачивал функцию в `staticmethod`. Это сделано для того, чтобы функция не сбаундилась с инстансом. В Python 3.7.1 `_wrap_strfunc` удалили ([вот этот коммит]((https://github.com/python/cpython/commit/62a99515301fa250feba1a2e0f2d8ea2a29d700e))).

Да, оно баундидтся как-то так:

```python
def f(*args):
    print(args)

class A:
    m = f

A.m()
# ()

A().m()
# (<__main__.A object at 0x7f79cc59a978>,)
```

Но есть тут один нюанс: built-in функции не баундятся:

```python
def my_max(*args):
    return max(*args)

class A:
    builtin_max = max
    my_max = my_max

A().builtin_max()
# TypeError: max expected 1 arguments, got 0

A().my_max()
# TypeError: 'A' object is not iterable
```

Поэтому когда eventlet подменяет open на [свой собственный](https://github.com/eventlet/eventlet/blob/7c21c8f92eed58c508f30defed133071c5728df7/eventlet/green/os.py#L101), всё ломается.
