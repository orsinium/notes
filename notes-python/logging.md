# Beautiful logging in Python

Hi everyone. I'm Gram. Today I wanna talk to you about the bad, the ugly and the good python logging.

First, I want to say a few words about logging structure.

+ Loggers expose the interface that application code directly uses. Logger defines set of handlers.
+ Handlers send the log records to the appropriate destination. Handler has list of filters and one formatter.
+ Filters filter log records.
+ Formatters specify the layout of log records in the final output.

Ok, how to configure it?

The bad. Just call some functions and methods. Exactly like in official documentation. Never do it. Never.

```python
import logging

logger = logging.getLogger('spam_application')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('spam.log')
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)
```

Next one, logging can be configured via ugly ini config.

```toml
[loggers]
keys=root,simpleExample

[handlers]
keys=consoleHandler

[formatters]
keys=simpleFormatter

[logger_simpleExample]
level=DEBUG
handlers=consoleHandler
qualname=simpleExample
propagate=0

[handler_consoleHandler]
class=StreamHandler
level=DEBUG
formatter=simpleFormatter
args=(sys.stdout,)

[formatter_simpleFormatter]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s

```

The good. Configure it via dict config. It's readable and little bit extendable. It's exactly how Django does it.

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'special': {
            '()': 'project.logging.SpecialFilter',
            'foo': 'bar',
        }
    },
    'handlers': {
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'myproject.custom': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
            'filters': ['special']
        }
    }
}

```

The perfect. Store this dict in toml file. It's readable, extandable, standartized.

```toml
version = 1
disable_existing_loggers = false

[formatters.json]
format = '%(levelname)s %(name)s %(module)s %(lineno)s %(message)s'
class = 'pythonjsonlogger.jsonlogger.JsonFormatter'

[filters.level]
"()" = "logging_helpers.LevelFilter"

[handlers.stdout]
level = "DEBUG"
class = "logging.StreamHandler"
stream = "ext://sys.stdout"
formatter = "simple"
filters = ["level"]

[handlers.json]
level = "DEBUG"
class = "logging.StreamHandler"
stream = "ext://sys.stdout"
formatter = "json"

[loggers.project]
handlers = ["stdout"]
level = "DEBUG"
```

And there is how you can use it. Thank you.
