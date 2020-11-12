# Python linters and formatters

## Linters

+ [pyflakes](https://github.com/PyCQA/pyflakes) -- checks only obvious bugs and never code style. There are no opinionated checks. Pyflakes must be enabled in any project, and all error must be fixed.
+ [pycodestyle](https://github.com/PyCQA/pycodestyle) -- most important code style checker. Controls compatibility with [PEP-8](https://www.python.org/dev/peps/pep-0008/) that is standard de-facto for how Python code should look like. Initially, with tool was called pep8, but [renamed after Guido's request](https://github.com/PyCQA/pycodestyle/issues/466).
+ [flake8](https://gitlab.com/pycqa/flake8) is the most famous Python linter. First of all, it is a framework allowing to write your own linters that can be configured and run in a unified way. Pyflakes and pycodestyle are default dependencies of Flake8. If you just install and run Flake8 in clean environment, you'll see their checks.
+ [flakehell](https://github.com/life4/flakehell) is a wrapper around flake8. It provides additional commands and features, nicer output, and more control over plugins and checks.
+ [PyLint](https://github.com/PyCQA/pylint) is an alternative linter with many checks that are missed in flake8 plugins. Some of them is opinionated and can be difficult to satisfy. However, most of the checks are really useful. FlakeHell supports PyLint as a plugin. The important thing to remember is that PyLint is slow because of heavy inference of types and values.
+ [wemake-python-styleguide](https://github.com/wemake-services/wemake-python-styleguide) is a flake8/flakehell plugin, providing a lot of checks. It is fast, strict, and helpful, finds many bugs, style issues, enforces consistency. It is very opinionated, so you probably want to disable some (most of the) checks.

See [awesome-flake8-extensions](https://github.com/DmytroLitvinov/awesome-flake8-extensions) for more plugins.
