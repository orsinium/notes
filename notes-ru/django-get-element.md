# О выборке данных в Django ORM

## Принцип обработки основных методов

Важное примечание по работе кеша:

1. Выборка данных из БД кешируется.
1. Кеш для queryset'а не устаревает и никуда не девается.
1. Методы, изменяющие запрос (типа filter или only), возвращают новый queryset с пустым кешем.

И ещё кое-что: принцип работы описан для Django 2.0. Об этом чуть ниже.

### queryset.get()

1. Вызывает queryset.filter с переданными параметрами.
1. Проверяет len(queryset).
1. Возвращает первый объект из кеша.

### len(queryset)

1. Выбирает данные из БД
1. Возвращает размер закешированных данных

Аналогичен len(list(queryset))

### bool(queryset)

1. Выбирает данные из БД
1. Возвращает bool от закешированных данных

Аналогичен bool(list(queryset))

### queryset[n]

1. Устанавливает для запроса `LIMIT n, n+1`.
1. Выбирает данные из БД.
1. Возвращает первый объект из кеша.

### queryset[start:stop:step]

1. Устанавливает для запроса `LIMIT start, stop`.
1. Выбирает данные из БД.
1. Возвращает список объектов из кеша с примененным к ним step (`list(qs)[::k.step]`).

### queryset.first()

1. Если queryset не отсортирован, сортирует его по pk.
1. Берет срез до первого элемента от queryset (queryset[:1])
1. Возвращает первый объект из queryset'а, если он там есть, иначе -- None.


## Как быстро выбрать первый элемент?

Вопрос, какзалось, простой, однако из версии к версии в Django многое менялось, и ответ сильно зависит от используемой версии.  

### Django 1.8 и выше

```python
queryset.first()
```

Также важно отметить, что в Django срез с шагом [возвращает](https://github.com/django/django/blob/2.0/django/db/models/query.py#L302) список, а без шага -- queryset. Устанавливать `LIMIT` для queryset'а можно несколько раз, и это даже [будет работать](https://github.com/django/django/blob/2.0/django/db/models/sql/query.py#L1603).

### Django 1.6 и 1.7

В этой версии Django метод first работает не оптимально. Он выбирает **весь** queryset из БД. Поэтому сначала его нужно ограничить.

```python
queryset[:1].first()
```

### Django 1.5 и младше

В этой версии Django метод first отсутствует.

Через условия:

```python
q = queryset[:1]
return q[0] if q else None
```

Либо через исключения:

```python
try:
    return queryset[:1].get()
except ModelName.DoesNotExist:
    return
```
