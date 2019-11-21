# Why does Python have colon?

Python has a colon (`:`) after all statements that start a new block: `if`, `for`, `while`, `def`, `class`, `with`, `else`. For example:

```python
if a == 1:
    b = 2
```

However, colon looks redundant. Both a machine and a human can understand that a new block started by indentation, and you can't miss that block anyway. For example above it could look like this:

```python
if a == 1   # SyntaxError
    b = 2
```

So, why do we need it?

## Lambda

Python has this colon from the very first release v.0.9.0 in February 1991. The standard library at this point was more proof of concept what you can do on Python either something handful. Since then, only a few modules survived: [calendar](https://docs.python.org/3/library/calendar.html), [dis](https://docs.python.org/3/library/dis.html), [fnmatch](https://docs.python.org/3/library/fnmatch.html), [glob](https://docs.python.org/3/library/glob.html), `path` (now it's [os.path](https://docs.python.org/3/library/os.path.html)), [shutil](https://docs.python.org/3/library/shutil.html), and `wrandom` (now it's [random](https://docs.python.org/3/library/random.html)). And even they, of course, have changed a lot.

The most ineresting and useless module was `lambda.py`. It contained an implementation of some lambda calculus functions. Lambda calculus is an incredibly fun exercise when you implement the whole functional programming language using only lambdas. If you're not familiar with the conception, I really recommend David Beazley's workshop [Lambda Calculus](https://youtu.be/5C6sv7-eTKg). But let's move on.

Python until version 1.0.0 released in January 1994 didn't have lambda expression. So, how it could do lambda calculus without lambdas? Let's see. There is an implementation of `3` [church number](https://en.wikipedia.org/wiki/Church_encoding) from that module:

```python
def Thrice(f, x): return f(f(f(x)))
```

Right, that's just a function, but to look more like lambda it's written in one line. It's possible to parse such case because indentation isn't the only one feat of the code block, but also we have a colon. And it works for all Python versions, from the first release. And that release used this feature a lot. Let's see a few more examples from the standard library (0.9.0).

A function with inlined cycle:

```python
def norm(a, n, p):
  a = poly.modulo(a, p)
  a = a[:]
  for i in range(len(a)): a[i] = mod(a[i], n)
  a = poly.normalize(a)
  return a
```

A fun hack to get `None` without having literal for it:

```python
# Name a constant that may once appear in the language...
def return_nil(): return
nil = return_nil()
```

A long chain of `if`'s from built-in text adventure:

```python
def decide(here, cmd):
  key, args = cmd[0], cmd[1:]
  if not args:
    if key = N: return here.north()
    if key = S: return here.south()
```

Important note: all examples from earliest Python release, and nobody really talked about code style at that moment. 10 years ago was introduced [PEP-8](https://www.python.org/dev/peps/pep-0008/) that clearly recommends to avoid such inlining:

> Compound statements (multiple statements on the same line) are generally discouraged.
> While sometimes it's okay to put an if/for/while with a small body on the same line, never do this for multi-clause statements. Also avoid folding such long lines!

I'd like to be stricter here: never use it. It always makes code more difficult to read. Python is a bad language for saving lines of code or even chars, you can save much more space by using Perl, for example.

## ABC

Python syntax was heavily influenced by [ABC](https://en.wikipedia.org/wiki/ABC_programming_language) language. And the colon is one of many things that was copied from ABC into Python. However, ABC had no such application for colon and didn't support blocks inlining. So, the real motivation behind the colon was not inlining, but something different. An example of the ABC syntax from Wikipedia:

```
HOW TO RETURN words document:
   PUT {} IN collection
   FOR line IN document:
      FOR word IN split line:
         IF word not.in collection:
            INSERT word IN collection
   RETURN collection
```

Let's see a papers that was published by ABC authors while the language was only in the stage of idea, even before the first implementation (that was named `B0`). I think, "Designing a beginners' programming language" is a most interesting and essential one, but the next statement correct for all their papers from that period. All code examples had no colon. For example:

```
FOR I OVER ROW
  FOR J OVER COL
    PUT 0 IN A(I, J)
```

[Lambert Meertens](https://en.wikipedia.org/wiki/Lambert_Meertens), one of designers of ABC, had a small talk at [CWI Lectures 2019](https://www.cwi.nl/events/2019/lectures-2019/cwi-lectures-2019) about ABC and it's influence on Python. After the talk I asked him about the moment when and why they came to the idea of the colon. And he told me a story.

It was the late evening, they were staying around a blackboard a little bit drunk and thinking about the syntax of the future language. They wrote down an implementation of bubble sort in a few different syntax. And now was the question, how to choose the best one. One way is to run tests in the head, how they did it, but that was not enough for a language "designed for beginners", hey also needed a user test. So, they asked for help a woman that worked there. I'm not sure who she was by specialty, but definitely not developer at all. She had a long look at blackboard and said that she doesn't understand any implementation. They explained it a bit, and she said: "Oooh, now I've got it. That `if` line not only about this line itself, but also contains the code after it". They said "yes" and as solution added a colon after `if` and `for` lines. The colon is used in natural language: for explanation, and enumeration, even in this sentence. And it made that moment clear for her.

So, the colon helps to write code in one line, and was added in ABC (and then in Python) for one non-developer person a long time ago to make it more similar to the natural language.
