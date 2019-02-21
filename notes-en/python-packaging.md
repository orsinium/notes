# Python packaging for your team

I love [decoupling](https://bit.ly/2m07ZOj). This makes the project maintaining easier. We have 2 main ways to do it:

1. [Git submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules). This is a good conception but sometimes very confusable. Also, you must commit updates in parent project for each submodule changing.
2. Packaging. I think this solution is better because you already use many packages in your project. You can easily package your project and explain this concept to any junior.

This article about creating [python package](https://packaging.python.org/) without pain.


## Setuptools

Most python packages which you are using contain [setup.py](https://packaging.python.org/tutorials/packaging-projects/#creating-setup-py) file in its root directory. This file describes package name, version, requirements (required third-party packages), package content and some optional information. Just call `setuptools.setup(...)` with this info as kwargs. It's enough for package distribution. If you have setup.py then you already can distribute it. For example, upload into [pypi.org](https://pypi.org/).


## Pip and virtualenv

[Pip](https://pip.pypa.io/en/stable/) -- de facto standard approach for installing python packages in your system. Simple and well known.

By default, pip installs all packages for all users in the system and requires root privileges for it. [Don't sudo pip](https://pages.charlesreid1.com/dont-sudo-pip/). Use virtualenv to install packages into isolated environments. Besides security troubles, some packages may have incompatible required versions of some mutual package.

Also I recommend to use [pipsi](https://github.com/mitsuhiko/pipsi) for some global entry points like [isort](https://github.com/timothycrosley/isort). Yeah, pipsi uses virtualenv.



## Editable packages

Sometimes you want to get actual package version directly from your other repository. This is very useful for non-distributable projects. Setuptools doesn't support it, but you can do it via pip:

```bash
pip install -e git+git@bitbucket.org:...git@master#egg=package_name
```

And you can pin this and any other requirements into [requirements.txt](https://caremad.io/posts/2013/07/setup-vs-requirement/):

```
-e git+git@bitbucket.org:...git@master#egg=package_name
...
deal
Django>=1.11
...
```

Also, pip supports constraints.txt with the same syntax for pinning versions for optional dependencies:

```
djangorestframework>=3.5
```

To install these dependencies just pass them into pip:

```bash
pip install -r requirements.txt -c constraints.txt
```

Requirements.txt is very useful when you don't want to create setup.py for your internal projects.


## Pip-tools

In most commercial projects you have at least 2 environments:

1. Development. Here you can get last available packages versions, develop and test project with it.
2. Production. Here you are able to create the same environment as where you're testing this code. And these requirements must not be updated while you're not testing and improving your code for changes in new versions. Also, other developers are able to get the same environment as you, because it's already tested and this approach is saving their time.

[Pip-tools](https://github.com/jazzband/pip-tools) provide some tools for this conception.


## Pipfile and pipenv

Pip developers decided to [improve requirements.txt](https://github.com/pypa/pip/issues/1795) for grouping dependencies and enabling native support for version locking. As a result, they have created [Pipfile specification](https://github.com/pypa/pipfile) and [pipenv](https://docs.pipenv.org/) -- a tool for working with it. Pipenv can lock versions in [Pipfile.lock], manage virtual environments, install and resolve dependencies. So cool, but for distributable packages, you must duplicate main dependencies into setup.py.


## Poetry

[Poetry](https://github.com/sdispater/poetry) -- beautiful alternative to setuptools and pip. You can just place all package info and all requirements into [pyproject.toml](https://poetry.eustace.io/docs/pyproject/). That's all. Beautiful. But poetry has some problems:

1. It's not compatible with setuptools. As a result, your users can't install your project without poetry. Everybody have setuptools, but many users don't know about poetry. You can use it for your internal projects, but poetry can't install dependencies from file or repository without `pyproject.toml` generating. Yeah, if you fork and improve some project, you must make [sdist](https://docs.python.org/3/distutils/sourcedist.html) for any changes and bump version for all projects that depend on it. Or manually convert project's `setup.py` to `pyproject.toml`.
2. Poetry [doesn't creates a virtual environment](https://poetry.eustace.io/docs/basic-usage/#poetry-and-virtualenvs) if you already into virualenv. So, poetry doesn't create an environment if you install poetry via pipsi. Pipenv, as opposed to poetry, always creates a virtual environment for a project and [can choose the right python version](https://docs.pipenv.org/advanced/#automatic-python-installation).
3. Poetry use [version specifiers](https://poetry.eustace.io/docs/versions/#version-constraints) incompatible with [PEP-440](https://www.python.org/dev/peps/pep-0440/#version-specifiers). This makes me sad.

For backward compatibility, you can generate setup.py and requirements.txt from pyproject.toml via [poetry-setup](https://github.com/orsinium/poetry-setup).


## Flit

If pyproject.toml is cool, why only poetry use it? Not only. [Flit](https://github.com/takluyver/flit) supports pyproject.toml too. This is a very simple tool with only 4 commands:

1. **init** -- interactively create pyproject.toml.
2. **build** -- make sdist or wheel.
3. **publish** -- upload package into PyPI (or another repository).
4. **install** -- install a local package into the current environment.

That's all. And enough in common cases. Flit uses pip for packages installation. And flit listed in [alternatives by PyPA](https://packaging.python.org/key_projects/?#flit). As in poetry, you need to manage virtual environments by other tools. But this package has a significant disadvantage: flit can't lock dependencies.


## Let's make the best packaging for your team!

All solutions below have some problems. Let's fix it!


### Poetry based packaging

1. Always create a virtual environment for each project. I recommend to use [pew](https://github.com/berdario/pew) or [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/) for better experience.
2. Use [pyenv](https://github.com/pyenv/pyenv) or [pythonz](https://github.com/saghul/pythonz) for python versions managing. Also, I recommend try to use [pypy](https://pypy.org/) for some of your small and well-tested projects. It's really fast.
3. Sometimes you want to depend on some setuptools-based projects on some package. Use [poetry-setup](https://github.com/orsinium/poetry-setup) for compatibility with it.


### Pipfile or requirements.txt based packaging

As we remember, with pipenv we need to duplicate all requirements in old format for setup.py. Let's improve it! I've created [install-requires](https://github.com/orsinium/install-requires) project that can help you convert requirements between formats. But which format should you choose?

1. `requirements.txt`. This is the most popular requirements format for projects. Anyone can use it as they want.
2. `Pipfile.lock`. Pipenv has better requirements lock than pip-tools, and you should use it for better security. But if you want to create a package from a project, then you plan to use this package into other projects. So, if this project depends on more than one package with locked requirements, pipenv can't resolve these dependencies. For example, one package lock `Django==1.9` version, but other uses `Django==1.11`. Do not use it for distributable packages: PyPA recommends to [place not locked versions into install_requires](https://packaging.python.org/discussions/install-requires-vs-requirements/).
3. `Pipfile`. This is our choice. Modern format with some problems, but also with many features. And, most importantly, simple and comfortable. I recommend using it for internal python packages in your company.

Install-requires repository contains [example](https://github.com/orsinium/install-requires/blob/master/example/setup.py) how you can convert requirements from Pipfile to setup.py compatible format on the fly.


## Setuptools is dead?

Many developers (me too) love poetry because it uses beautiful project metadata describing format as setup.py alternative. But setuptools allows you to [use setup.cfg instead of setup.py](https://setuptools.readthedocs.io/en/latest/setuptools.html#configuring-setup-using-setup-cfg-files) and it's also beautiful. Furthermore, [isort](https://github.com/timothycrosley/isort) and [flake8](http://flake8.pycqa.org/en/latest/) supports setup.cfg too.

Setuptools supports requirements from VCS, file or archive via [dependency_links parameter](https://setuptools.readthedocs.io/en/latest/setuptools.html#dependencies-that-aren-t-in-pypi). And requirements grouping via [extras_require](https://setuptools.readthedocs.io/en/latest/setuptools.html#declaring-extras-optional-features-with-their-own-dependencies).

So, what's wrong with setuptools? I think this tool has some problems:

1. No native virtualenv and python version managing. And poetry can't do it too. But we have pew, virtualenvwrapper, pyenv, pythonz, and many other useful tools. This is UNIX-way.
2. No dependencies locking. Poetry, pipenv, and pip (`pip freeze`) can lock dependencies from its own files. Setuptools can't. This is because of setuptools for packages, not projects.
3. Setup.cfg is good, but [pyproject.toml better](https://github.com/pypa/packaging-problems/issues/29#issuecomment-375845650). Setuptools [will support pyproject.toml](https://github.com/pypa/setuptools/issues/1160) and deprecate setup.py and setup.cfg. Also [pip will support it too](https://pip.pypa.io/en/stable/reference/pip/?highlight=pyproject.toml%20#build-system-interface). And it's cool!


## Further reading

1. For pros and cons see issues for projects from article:
    1. [poetry](https://github.com/sdispater/poetry/issues?q=is%3Aopen+is%3Aissue+label%3Aenhancement)
    1. [pipenv](https://github.com/pypa/pipenv/issues?q=is%3Aopen+is%3Aissue+label%3Aenhancement)
    1. [setuptools](https://github.com/pypa/setuptools/issues?q=is%3Aopen+is%3Aissue+label%3Aenhancement)
1. [How to install other Python version](https://realpython.com/installing-python/) (sometimes you don't need pyenv).
1. [Installing packages using pip and virtualenv](https://packaging.python.org/guides/installing-using-pip-and-virtualenv/).
1. [Beautiful example for setuptools configuring via setup.cfg](https://github.com/4383/sampleproject/blob/c503301e4b381790e5a9125c3dd636921052e8e1/setup.cfg).
1. [Setuptools documentation](https://setuptools.readthedocs.io/en/latest/setuptools.html).
1. [install_requires vs requirements files](https://packaging.python.org/discussions/install-requires-vs-requirements/).


## Further reading (RUS)

1. [About poetry](https://t.me/itgram_channel/152).
1. [About PyPy and python dev environment](https://t.me/itgram_channel/97).
1. [About toml format](https://t.me/itgram_channel/113).
