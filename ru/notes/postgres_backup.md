# Бэкапим PostgreSQL


1. Устанавливаем PostgreSQL:
    ```bash
    apt update
    apt install postgresql
    ```
1. Создаем [.pgpass](https://www.postgresql.org/docs/9.2/static/libpq-pgpass.html) файл, чтобы `pg_basebackup` знал, какой использовать пароль:
    ```bash
    nano .pgpass
    ```
    Добавляем туда данные для подключения:
    ```
    1.1.1.1:6432:*:backup:PASSWORD
    ```
1. Прячем наши пароли ото всех:
    ```bash
    chmod 600 .pgpass
    ```

WIP
