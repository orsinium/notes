# Особенности Unicode и алфавитов, которые стоит знать.

## Homoglyphs

В математике есть много символов, похожих на буквы латинского алфавита. А ещё есть emoji. Зовут их [letterlike symbols](https://en.wikipedia.org/wiki/Letterlike_Symbols), и они могут создавать некоторые проблемы (об этом ниже).

Но кроме них есть так называемые [Homoglyphs](https://en.wikipedia.org/wiki/Homoglyph) -- похожие буквы. Или вообще одинаковые. Или не буквы. Например, вы знаете, что "с" может быть как русской буквой "эс", так и английской "си". И пишутся они совершенно одинаково.

Ребята из Unicode Consortium заботятся, чтобы нам было не слишком больно, и [собрали полный список](http://www.unicode.org/Public/security/latest/) символов, которые могут делать больно.


## Алфавиты

Однозначно определить язык по одной букве не получится. Символы Uncode [разбиты на группы](https://en.wikipedia.org/wiki/ISO_15924#List_of_codes) которые я для простоты называю категориями. Группы соответствуют алфавитам, и в одном языке используется лишь часть символов из алфавита, а один алфавит используют множество языков. Например, [кириллический алфавит](https://ru.wikipedia.org/wiki/%D0%90%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%8B_%D0%BD%D0%B0_%D0%BE%D1%81%D0%BD%D0%BE%D0%B2%D0%B5_%D0%BA%D0%B8%D1%80%D0%B8%D0%BB%D0%BB%D0%B8%D1%86%D1%8B) используется в [русском](https://ru.wikipedia.org/wiki/%D0%A0%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B9_%D1%8F%D0%B7%D1%8B%D0%BA), [украинском](https://ru.wikipedia.org/wiki/%D0%A3%D0%BA%D1%80%D0%B0%D0%B8%D0%BD%D1%81%D0%BA%D0%B8%D0%B9_%D1%8F%D0%B7%D1%8B%D0%BA), [белорусском](https://ru.wikipedia.org/wiki/%D0%91%D0%B5%D0%BB%D0%BE%D1%80%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B9_%D1%8F%D0%B7%D1%8B%D0%BA) и прочих языках. Всего в Unicode 421 символ в кириллице и 1299 -- в латинском алфавите.


## Зачем это всё знать?

Такие символы позволяют делать довольно жестокие вещи:

1. [Ломать код](https://github.com/reinderien/mimic).
2. Регистрировать фишинговые ресурсы: [пример](https://xakep.ru/2016/11/22/referral-spam/) и [описание атаки](https://en.wikipedia.org/wiki/IDN_homograph_attack).
3. [Обходить защиту от SQL инъекций](https://hackernoon.com/%CA%BC-%C5%9B%E2%84%87%E2%84%92%E2%84%87%E2%84%82%CA%88-how-unicode-homoglyphs-will-break-your-custom-sql-injection-sanitizing-functions-1224377f7b51)

Ну и тупо человек может перепутать буквы. Например, при вводе промокода, какого-то ключика или [пароля от Wi-Fi](https://www.youtube.com/watch?v=XNMOYFArkTc).


## Python

В стандартной библиотеке Python есть [unicodedata](https://docs.python.org/3/library/unicodedata.html) -- модуль для получения информации о unicode-символе. Собственно, это все его возможности.

А ещё есть библиотека [confusable_homoglyphs](https://github.com/vhf/confusable_homoglyph). не используйте её. Наверное, это худшее, что я видел написанное на Python. У меня есть немного аргументов:
1. Оно не работает. Просто попробуйте вот это:
  ```python
  from confusable_homoglyphs import confusables
  confusables.is_confusable('Д', preferred_aliases=['latin'])
  ```
  Спойлер:
  ```
  TypeError: 'NoneType' object is not iterable
  ```
2. Автору кажется, что [бинарный поиск по связанному списку](https://github.com/vhf/confusable_homoglyphs/blob/master/confusable_homoglyphs/categories.py#L27) -- это весело. Нет, не весело.
3. Вся огромная БД выгружается в ОЗУ.

В общем, много проблем. Я сделал круто:
[homoglyphs](https://github.com/orsinium/homoglyphs). Умеет работать с языками, алфавитами, гомоглифами, выгружать в память только нужные данные (а заодно так можно отфильтровать ненужные гомоглифы), конвертировать гомоглифы в ASCII.


## Другие языки

[https://github.com/codebox/homoglyph] -- библиотека для Java и Java Script, в которой используется []список гомоглифов](https://github.com/codebox/homoglyph/blob/master/raw_data/chars.txt), распарсенный с помощью скрипта на Python. Видно, автор очень любит языки программирования. Можете использовать. Как минимум, можно забрать распарсенный файлик.
