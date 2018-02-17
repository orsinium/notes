Login and dump cookies:

```bash
curl -X POST -c cookies.txt -u "user1:password1" myserver.com/login
```

GET JSON:

```bash
curl https://restcountries.eu/rest/v1/name/france | python -m json.tool
```

Show request's headers:

```bash
curl -sD - -o /dev/null ya.ru
```

