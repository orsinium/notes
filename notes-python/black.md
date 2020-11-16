# Don't use Black in your team

[Black](https://github.com/python/black) is a quite popular autoformatter for Python code. Author of black ([ambv](https://github.com/ambv)) is a Python core developer. In May 2019 black bacame Python's official tool. Sounds cool, doesn't it? I really love autoformatting (especially [go format](https://blog.golang.org/go-fmt-your-code)), it allows yout to forget about code styles and avoid [bikeshedding](http://bikeshed.com/), but in the same time keep your code beautiful, readable and consistent. And I'm not recommend you to use Black for a while.

## It's incompatible with Flake8

Flake8 is a most popular linter for Python. Flake8 has [3.5kk downloads](https://pypistats.org/packages/flake8) in this month, while Black [0.6kk downloads](https://pypistats.org/packages/black). Flake8 is linter, Black is a fromatter, so why not to use both at the same time?

1. [Pycodestyle has old bug](https://github.com/PyCQA/pycodestyle/issues/373) that forbid whitespaces inside slices, while Black adds these spaces.
1. Black is incompatible with many Flake8 plugins, I will show some of them below.

## It's about consistency, not readability

Black tries to have opinion about everything. Every situation must have one and only one solution how it format:

>  It doesn't take previous formatting into account.

For example, it tries to fit everything in one line. In many cases you don't want it:

1. When you have one element per-line it's easier to keep elements sorted. For example, [sort-lines](https://github.com/atom/sort-lines) for Atom. One-liner you have to sort manually.
1. Sometimes you want to add comments to elements. For example:

```python
# formatted by smart developer:
ignore = [
  'dist',   # distribution archives
  'build',  # builded project for current OS
]

# formatted by black:
ignore = ["dist", "build"]  # distribution archives  # builded project for current OS
```

## Trailing commas

Black always drops trailing commas from everything. Trailing commas in multiline statements makes adding new elements easier and diffs clean. Read [Why you should enforce Dangling Commas for Multiline Statements](https://medium.com/@nikgraf/why-you-should-enforce-dangling-commas-for-multiline-statements-d034c98e36f8) for details.

```python

# beautiful
'very-very long {subject} (or {subject_alt})'.format(
    subject='line',
    subject_alt='other piece of text',
)

# black
"very-very long {subject} (or {subject_alt})".format(
    subject="line", alt="other piece of text"
)
```

Additionally, without triling commas you can forget to add comma to the previous element, and interpreter will ok with it because of [implicit string concatenation](https://www.python.org/dev/peps/pep-3126/). And for Black [it's valid syntax](https://github.com/python/black/issues/26) too:

```python
# ups, I forgot a comma:
(
  '1',
  '2'
  '3'
)

# thank you, black:
("1", "2" "3")
```

I recommend you to use trailing commas for multiline statements and control it with [flake8-commas](https://github.com/PyCQA/flake8-commas) plugin for flake8.

## It's not configurable... Or not?

Another piece of Black philosophy:

> It is not configurable.

This is main conception of Black, and it doesn't work after all. Now Black has flags to configure line length and quotes style. This is because this philosophy doesn't work while tool isn't good enough. Maybe, some day, but not in the current state. It makes much troubles:

1. If you found a bug in Black, you can't disable one particular check for your project to continue using of Black on the project while bug is not fixed. And you will find many of bugs while Black is young.
1. You cannot adopt it for your current codestyle.
1. You cannot combine it with current linters without disabling checks in these linters.
1. You cannot integrate Black in your project step-by-step, enabling every check one-by-one.

## Ugly config

This is example from Black docs:

```python
[tool.black]
target-version = ['py37']
include = '\.pyi?$'
exclude = '''

(
  /(
      \.eggs         # exclude a few common directories in the
    | \.git          # root of the project
    | \.hg
    | \.mypy_cache
    | \.tox
    | \.venv
    | _build
    | buck-out
    | build
    | dist
  )/
  | foo.py           # also separately exclude a file named foo.py in
                     # the root of the project
)
'''
```

I never understand what the strange construction is it. Now I got it. It's regular expression! Why not a list of regexps? Ugh...

## It's not extendable

Another point of Black's philosophy is "there is only one style". So, it's against of plugins and any extendability: you cannot have any other rules except built-in in Black. And you can't disable them, of course. However, Black can't take care about everything. For example, using `.format` inside of log messages is a bad practice. Flake8 has plugin for it ([flake8-logging-format](https://github.com/globality-corp/flake8-logging-format)), but will we ever see this check in Black? I don't think so.

## There is no warnings

Black only do changes. It can't give you feedback or make some changes that can affect your interfaces. For example, Flake8 has [flake8-mutable](https://github.com/ebeweber/flake8-mutable) plugin that prevents you from using mutable default arguments for function. Black can't do anything with it.

## It's one person decisions

Ambv has done a great work. However, it's one-person project, as most of Open Source projects. Flake8 plugins made by different people and teams. You can think that these rules is incompatible, goes from different styleguides and you can't combine these plugins together. It's not true. I'm using almost all Flake8 plugins, and I have no experience when 2 plugins had different opinion about some code.

## It's still in beta

The Black documentation [explicitly states](https://github.com/psf/black#note-this-is-a-beta-product) that the project is still in beta test. From the practical perspective, that means that the code style changes in every release. So, if you want to use it in a project, be ready to take an actions:

1. Lock the exact version of Black in your dependencies file.
1. When you upgrade to a newer version of black, be ready to reformat all the code. Keep in mind that it will complicate backports and cause a few git merge conflicts.
1. Make sure that everyone in the project uses exactly the same version of black. Explicitly ask everyone to upgrade black when its version in the project was changed.
1. If you enforce Black on CI, it's better to make the job optional (`allow_failure: true`). Otherwise, it will even more complicate backports and black version upgrade.

## Alternatives

Ok, let's talk about alternatives and when Black is a good choice.

1. Have a big ugly codebase that you want to make readable for yourself? Use [black](https://github.com/python/black).
1. Don't want to think about formatting for your little project? Use [black](https://github.com/python/black).
1. Have a big codebase that you can adopt for your codestyle? Use [yapf](https://github.com/google/yapf).
1. Do you want to improve your productivity working in an experienced team? Use [autopep8](https://github.com/hhatto/autopep8).
1. Want to have beautiful and consistent code in your team or big project? Enable [flake8](http://flake8.pycqa.org/en/latest/) on CI and add as much [flake8 plugins](https://github.com/DmytroLitvinov/awesome-flake8-extensions) as you can. Also, I recommend to have a look on [wemake-python-styleguide](https://github.com/wemake-services/wemake-python-styleguide) -- biggest collection of Flake8 rules.
