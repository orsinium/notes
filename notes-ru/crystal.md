# Crystal

Сегодня у нас язык программирования [Crystal](https://crystal-lang.org/)

Плюсы: скорость, простое написание, надёжность.
Минусы: сложно читать, высокий порог вхождения.

Особенности:
+ Синтаксис как у Ruby
+ Статическая типизация с дженериками
+ Выведение типов
+ Быстрый и компилируемый
+ Простые и быстрые C-биндинги
+ Ассемблерные вставки (если вдруг хотите написать драйвер)
+ Тонны синтаксического сахара и концепций
+ Сборщик мусора
+ Макросы

Язык перегружен концепциями и синтаксическим сахаром, которые можно просто выкинуть. Нет, серьёзно, это самый перегруженный язык. Сами смотрите: 6 способов написать if-else, 6 способов создать один и тот же список и тонны литералов (я даже не могу сосчитать). А ещё отдельные типы данных для строковых констант, range, регулярных выражений, shell команд, анонимных функций, enums. Большая часть этого для того, чтобы было проще писать код. Например, вместо ["one", "two", "three"] можно написать %w(one two three). Удобно, но это увеличивает порог входа (я без понятия, как это всё вообще запомнить) и жутко усложняет чтение кода.

Несмотря на то, что Crystal зарелизили в 2014 году, у него уже есть неплохое комьюнити и экосистема. Например:

+ ameba (https://github.com/crystal-ameba/ameba) — линтер
+ kemal (https://github.com/kemalcr/kemal) — web фреймворк (на самом деле, далеко не единственный)
+ crecto (https://github.com/Crecto/crecto) — ORM
+ crystal-pg (https://github.com/will/crystal-pg) — драйвер для PostgreSQL
+ crystal-redis (https://github.com/stefanwille/crystal-redis) — драйвер для Redis

А вообще, C-биндинги в Crystal довольно простые, поэтому если какой-то библиотеки не хватает, можно подтянуть из C.

Ссылки по теме:
+ Официальная документация (https://crystal-lang.org/reference/)
+ Репозиторий (https://github.com/crystal-lang/crystal)
+ My favorite things in Crystal Lang (https://dev.to/jwoertink/my-favorite-things-in-crystal-lang-ce9)

#crystal #language #coding
@orsinium