# Python linters and formatters

## Linters

+ [pyflakes](https://github.com/PyCQA/pyflakes) -- checks only obvious bugs and never code style. There are no opinionated checks. Pyflakes should be enabled in any project, and all errors must be fixed.
+ [pycodestyle](https://github.com/PyCQA/pycodestyle) -- most important code style checker. Controls compatibility with [PEP-8](https://www.python.org/dev/peps/pep-0008/) that is standard de-facto for how Python code should look like. Initially, the tool was called pep8, but [renamed after Guido's request](https://github.com/PyCQA/pycodestyle/issues/466).
+ [flake8](https://gitlab.com/pycqa/flake8) is the most famous Python linter. First of all, it is a framework allowing you to write custom linters that can be configured and run in a unified way. Pyflakes and pycodestyle are default dependencies of Flake8. If you just install and run Flake8 in a clean environment, you'll see their checks.
+ [flakehell](https://github.com/life4/flakehell) is a wrapper around flake8. It provides additional commands and features, nicer output, and more control over plugins and checks.
+ [PyLint](https://github.com/PyCQA/pylint) is an alternative linter with many checks that are missed in flake8 plugins. Some of them are opinionated and can be difficult to satisfy. However, most of the checks are useful. FlakeHell supports PyLint as a plugin. The important thing to remember is that PyLint is slow because of heavy inference of types and values.
+ [wemake-python-styleguide](https://github.com/wemake-services/wemake-python-styleguide) is a flake8/flakehell plugin, providing a lot of checks. It is fast, strict, and helpful, finds many bugs, style issues, enforces consistency. It is very opinionated, so you probably want to disable some (most of the) checks.

See [awesome-flake8-extensions](https://github.com/DmytroLitvinov/awesome-flake8-extensions) for more plugins.

## Formatters

Python has quite a few code formatters with different code style and philosophy behind.

There are 3 all-in-one code formatters, all of them are supported by VSCode out of the box:

+ [autopep8](https://github.com/hhatto/autopep8) is the oldest and the least opinionated Python code formatter. It formats the code to follow [PEP-8](https://www.python.org/dev/peps/pep-0008/) and nothing else. Under the hood, it uses the mentioned above [pycodestyle](https://github.com/PyCQA/pycodestyle). So, if the project passes pycodestyle (or flake8) checks, you can safely use autopep8.
+ [black](https://github.com/python/black) is "uncompromising" and opinionated code formatter. The code style is close to PEP-8 (there are few exceptions) but also it has an opinion about pretty much everything. It has some issues that make it a bad choice for an experienced team. However, it can be a good choice for an inexperienced team, an open-source project, or for quick formatting of an old and dirty code. See [Don't use Black in your team](https://articles.orsinium.dev/python/black/) for more information.
+ [yapf](https://github.com/google/yapf) is a code formatter from Google. Like black, it reformats everything. The main difference is that every small detail in yapf is configurable. It makes sense to use yapf for a project with a code style that is different from PEP-8. However, if you have a choice, prefer using PEP-8 for all projects.

A few small but helpful formatters:

+ [isort](https://github.com/PyCQA/isort) groups and sorts imports. Usually, the imports section in Python is quite messy, and isort brings an order here. It is a powerful tool and every stylistic decision there can be configured. Use isort.
+ [add-trailing-comma](https://github.com/asottile/add-trailing-comma) adds trailing commas to multiline function calls, function signatures, and literals. Also, it fixes indentation for closing braces.
+ [autoflake](https://github.com/myint/autoflake) removes unused imports and variables. It helps clean up a messed code.
+ [docformatter](https://github.com/myint/docformatter) formats docstrings according to [PEP-257](https://www.python.org/dev/peps/pep-0257/).
+ [pyupgrade](https://github.com/asottile/pyupgrade) changes the code to use newer Python features. It will replace old comprehensions style, old formatting via `%`, drop Unicode and long literals, simplify `super` calls, and much more.
+ [unify](https://github.com/myint/unify) formats string literals to use one style of quotes (single or double).

See [awesome-python-code-formatters](https://github.com/life4/awesome-python-code-formatters) for more tools.

## Integrations

+ Flake8 is famous and has integration (or a hacky described somewhere way to integrate) with everything.
+ [FlakeHell can pretend to be flake8 for integrations](https://flakehell.readthedocs.io/ide.html)
+ VSCode Python extension supports flake8, pylint, isort, autopep8, black, and yapf out of the box. Just select what you want to use.
+ To integrate something else, like a less popular code formatter, use [pre-commit](https://github.com/pre-commit/pre-commit).
