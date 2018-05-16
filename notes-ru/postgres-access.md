# Доступ к PostgreSQL извне через PGBouncer


## PostgreSQL

1. Подключаемся к PostgreSQL:
    ```bash
    su postgres
    psql
    ```
1. [Создаем пользователя](https://www.cyberciti.biz/faq/howto-add-postgresql-user-account/) для бэкапов:
    ```sql
    CREATE USER backup SUPERUSER PASSWORD 'PLACE YOUR PASSWORD HERE';
    ```
1. Делаем его [readonly](https://dba.stackexchange.com/questions/52691/how-can-i-create-readonly-user-for-backups-in-postgresql):
    ```sql
    ALTER USER backup set default_transaction_read_only = on;
    ```
1. Запоминаем MD5 хэш пароля нового пользователя (шучу, выписываем):
    ```sql
    use postgres
    SELECT usename, passwd FROM pg_shadow
    ```
1. Выходим из psql и идём добавлять доступ к юзеру со внешнего сервера через [HBA](https://www.postgresql.org/docs/8.1/static/client-authentication.html):
    ```bash
    nano /etc/postgresql/9.6/main/pg_hba.conf
    ```
1. Добавляем след. строку:
    ```
    host    all             backup          1.1.1.1/32        md5
    ```
    Вместо 1.1.1.1 указываем IP внешнего сервера.

На этом всё. Если у вас нет pgbouncer, то в настройках PostgreSQL [открываем доступ из внешней сети](https://blog.bigbinary.com/2016/01/23/configure-postgresql-to-allow-remote-connection.html) и [обновляем настройки](https://www.heatware.net/databases/postgresql-reload-config-without-restarting/).


## PGBouncer

1. Корректируем настройки pgbouncer:
    ```bash
    nano /etc/pgbouncer/pgbouncer.ini
    ```
    1. Открываем доступ из внешней сети: `listen_addr = *`
    1. Включаем использование файла HBA: `auth_type = hba`
    1. Указываем путь к файлу HBA: `auth_hba_file = /etc/postgresql/9.6/main/pg_hba.conf`
1. Добавляем в список паролей, используемых в pgbouncer, данные нового пользователя:
    ```bash
    nano /etc/pgbouncer/userlist.txt
    ```
    Добавляем:
    ```bash
    "backup" "MD5 хэш пароля"
    ```
1. Перезапускаем pgbouncer:
    ```bash
    service pgbouncer restart
    ```


## Проверка доступов

С внешнего сервера:
```
pgcli --host АДРЕС_СЕРВЕРА_БД --port 6432 --dbname ЛЮБАЯ_БД --username ЛОКАЛЬНЫЙ_ПОЛЬЗОВАТЕЛЬ
```
Вводим пароль, и должно быть отказано в коннекте. Значит, лишнего не расшарили.


С сервера БД:
```
pgcli --host localhost --port 6432 --dbname ЛЮБАЯ_БД --username ЛОКАЛЬНЫЙ_ПОЛЬЗОВАТЕЛЬ
```
Вводим пароль, и должен быть успешный коннект. Значит, текущие доступы не сломали.


С сервера бэкапов:
```
pgcli --host localhost --port 6432 --dbname ЛЮБАЯ_БД --username backup
```
Вводим пароль, и должен быть успешный коннект. Значит, новый доступ добавили.
